/*
 =============================================================
 Create Database
 =============================================================
 Script Purpose:
 This script creates a new database named 'cafe_database' after checking if it already exists. 
 If the database exists, it is dropped and recreated. 

 
 WARNING:
 Running this script will drop the entire 'cafe_database' database if it exists. 
 All data in the database will be permanently deleted. Proceed with caution 
 and ensure you have proper backups before running this script.
 */



SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE datname = 'cafe_database';


-- Drop database if it exists
DROP DATABASE IF EXISTS cafe_database;
-- Create the database
CREATE DATABASE cafe_database;


