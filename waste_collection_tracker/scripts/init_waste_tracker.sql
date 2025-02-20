-- ====================================================================
-- Drop the 'wastetracker' database if it exists
-- ====================================================================
DROP DATABASE IF EXISTS wastetracker;

-- ====================================================================
-- Create a new 'wastetracker' database
-- ====================================================================
CREATE DATABASE wastetracker;

-- ====================================================================
-- Drop the 'user', 'schedules', and 'reports' tables if they exist
-- ====================================================================
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.schedules;
DROP TABLE IF EXISTS public.reports;


-- ====================================================================
-- Reset the sequence for 'users' table to the max ID value
-- ====================================================================
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));

-- ====================================================================
-- Reset the sequence for 'schedules' table to the max ID value
-- ====================================================================
SELECT setval('schedules_id_seq', (SELECT MAX(id) FROM schedules));

-- ====================================================================
-- Reset the sequence for 'reports' table to the max ID value
-- ====================================================================
SELECT setval('reports_id_seq', (SELECT MAX(id) FROM reports));


TRUNCATE TABLE users RESTART IDENTITY;
TRUNCATE TABLE schedules RESTART IDENTITY;
TRUNCATE TABLE reports RESTART IDENTITY;