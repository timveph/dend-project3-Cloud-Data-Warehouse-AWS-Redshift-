# Introduction
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud (AWS). Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

----
# The Project
To build an ETL solution that extracts data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to.

----
# Source Data
Two datasets reside in S3. Here are the S3 links for each:

- **Song data**: s3://udacity-dend/song_data
- **Log data**: s3://udacity-dend/log_data

Log data json path: s3://udacity-dend/log_json_path.json

### Song Data 
Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID.
### Log Data
The second path consists of log files in JSON format based on the songs in the dataset above. The files contain app activity logs from the Sparkify music streaming app. The log files in the dataset you'll be working with are partitioned by year and month.

----
# Project Files
### dwh.cfg
Contains configuration information for the ETL process such as
- cluster
- IAM 
- S3 locations

### sql_queries.py
A definition of SQL queries which create, drop and insert data into tables. These queries are called by the two python programs below.

### create_tables.py
Establishes a connection and creates fact and dimension tables for the star schema in Redshift.

### etl.py 
Establishes a connection and loads data from S3 into staging tables on Redshift and then process that data into your analytics tables on Redshift.

----
# Staging Tables
The tables below will be used to hold the information from the S3 json files before the information is processed into the schema.

### staging_events
Hold the information from log files, the table contais the columns (artist_name, auth, first_name, gender, itemInSession, last_name, duration, level, artist_location, method, page varchar, registration, session_id, title, status, start_time, user_agent, user_id).

### staging_songs
Hold the information from the song files, the table contains the columns (num_songs, artist_id, artist_latitude, artist_longitude, artist_location, artist_name, song_id, title, duration, year).

----
# Schema
The schema used is a star schema 
### Fact Table
- **songplays** - records in event data associated with song plays 

### Dimension Tables
- **users** - users in the app
- **songs** - songs in music database
- **artists** - artists in music database
- **time** - timestamps of records in songplays broken down into specific units

----
# Run the process
To run the process, execute the two programs in order: 
1. create_tables.py
2. etl.py



