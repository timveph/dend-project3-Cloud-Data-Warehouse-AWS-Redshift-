import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "drop table if exists staging_events_table"
staging_songs_table_drop = "drop table if exists staging_songs_table"
songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists user_table"
song_table_drop = "drop table if exists song_table"
artist_table_drop = "drop table if exists artist_table"
time_table_drop = "drop table if exists time_table"

# CREATE TABLES
staging_events_table_create= ("""create table if not exists staging_events_table 
                                (artist_name varchar, auth varchar, first_name varchar 
                                , gender char, itemInSession int, last_name varchar 
                                , duration float4, level varchar, artist_location varchar 
                                , method varchar, page varchar, registration float, session_id int 
                                , title varchar, status int, start_time bigint, user_agent varchar 
                                , user_id varchar)
                                """)

#song data json
# example: 
#     {"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
staging_songs_table_create = ("""create table if not exists staging_songs_table 
                                (num_songs int, artist_id varchar not null, artist_latitude varchar 
                                , artist_longitude varchar, artist_location varchar, artist_name varchar
                                , song_id varchar not null, title varchar, duration float4, year int)
                                """)

songplay_table_create = ("""create table if not exists songplays 
                            (songplay_id int identity(0,1), start_time timestamp NOT NULL, user_id varchar NOT NULL 
                            , level varchar, song_id varchar NOT NULL, artist_id varchar NOT NULL 
                            , session_id varchar NOT NULL, artist_location varchar, user_agent varchar 
                            , PRIMARY KEY (songplay_id))""")

user_table_create = ("""create table if not exists users 
                        (user_id varchar PRIMARY KEY NOT NULL, first_name varchar, last_name varchar, gender char 
                        , level varchar)""")

song_table_create = ("""create table if not exists songs 
                        (song_id varchar PRIMARY KEY NOT NULL, title varchar, artist_id varchar NOT NULL 
                        , year int, duration float4)""")

artist_table_create = ("""create table if not exists artists 
                        (artist_id varchar PRIMARY KEY NOT NULL, artist_name varchar, artist_location varchar 
                        , artist_latitude varchar, artist_longitude varchar)""")

time_table_create = ("""create table if not exists time 
                        (start_time timestamp PRIMARY KEY, hour int, day int, week int, month int
                        ,year int, weekday varchar)""")


# STAGING TABLES

staging_events_copy = (""" copy staging_events_table FROM {} \
                            CREDENTIALS 'aws_iam_role={}' \
                            FORMAT AS JSON {} \
                            region 'us-west-2' \
                                """).format(config.get('S3','LOG_DATA'),
                                            config.get('IAM_ROLE', 'ARN'),
                                            config.get('S3','LOG_JSONPATH'))

staging_songs_copy = (""" copy staging_songs_table from {} \
                            CREDENTIALS 'aws_iam_role={}' \
                            FORMAT AS JSON 'auto' \
                            region 'us-west-2' \
                                """).format(config.get('S3','SONG_DATA'), 
                                            config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES
# Needed help reading timestamp in
#  - https://www.fernandomc.com/posts/redshift-epochs-and-timestamps/

songplay_table_insert = ("""insert into songplays 
                            (start_time, user_id, level, song_id, artist_id, session_id 
                            ,artist_location, user_agent) 
                             select   timestamp 'epoch' + se.start_time/1000 * interval '1 second',
                                      se.user_id,
                                      se.level,
                                      ss.song_id,
                                      ss.artist_id,
                                      se.session_id,
                                      se.artist_location,
                                      se.user_agent                                      
                            from staging_events_table se
                            left join staging_songs_table ss
                                on    (se.title = ss.title
                                      and  se.artist_name = ss.artist_name)
                            where (se.page='NextSong'
                                  and ss.song_id is not null)
                         """)


user_table_insert = ("""insert into users 
                            (user_id, first_name, last_name, gender, level) 
                        select distinct user_id,
                                        first_name,
                                        last_name,
                                        gender,
                                        level
                        from staging_events_table
                        where user_id IS NOT NULL
                     """)


song_table_insert = ("""insert into songs 
                            (song_id, title, artist_id, year, duration) 
                        select distinct song_id,
                                        title,
                                        artist_id,
                                        year,
                                        duration
                        from staging_songs_table
                     """)

artist_table_insert = ("""insert into artists 
                            (artist_id, artist_name, artist_location, artist_latitude, artist_longitude) 
                          select distinct artist_id,
                                          artist_name,
                                          artist_location,
                                          artist_latitude,
                                          artist_longitude
                          from staging_songs_table
                       """)

#date_part- https://docs.aws.amazon.com/redshift/latest/dg/r_Dateparts_for_datetime_functions.html
time_table_insert = ("""insert into time 
                            (start_time, hour, day, week, month, year, weekday) 
                        (select songplays.start_time,
                                date_part(h, songplays.start_time),
                                date_part(d, songplays.start_time),
                                date_part(w, songplays.start_time),
                                date_part(mon, songplays.start_time),
                                date_part(y, songplays.start_time),
                                date_part(dow, songplays.start_time)
                         from songplays)
                     """)

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
