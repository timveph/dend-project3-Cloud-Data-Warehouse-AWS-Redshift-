# dend-project3-Cloud Data Warehouse
As a data engineer, I built an ETL pipeline that extracts data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for the analytics team to continue finding insights in what songs their users are listening to. The project is based on a fictitious company called Sparkify with fictitious data. 

## Schema for Song Play Analysis
Using the song and log datasets, you'll need to create a star schema optimized for queries on song play analysis. This includes the following tables.

### Fact Table
**songplays** - records in log data associated with song plays i.e. records with page NextSong  
> **fields** - songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension Tables
**users** - users in the app  
> **fields** - user_id, first_name, last_name, gender, level  

**songs** - songs in music database  
> **fields** - song_id, title, artist_id, year, duration  

**artists** - artists in music database  
>**fields** - artist_id, name, location, latitude, longitude  

**time** - timestamps of records in songplays broken down into specific units  
>**fields** - start_time, hour, day, week, month, year, weekday


## Project steps
### Create Table Schemas
1. Design schemas for fact and dimension tables
2. Write a SQL CREATE statement for each of these tables
3. Using Python, create the logic to connect to the database and create the tables

### Setup the data warehouse on AWS
1. Launch a redshift cluster and create an IAM role that has read access to S3.
2. Add the details of the redshift cluster and IAM role to a config file (dwh.cfg)

### Build ETL Pipeline
1. Load data from S3 to staging tables on Redshift
2. Load the data from the staging tables to the analytic tables in Redshift

### Document the process
