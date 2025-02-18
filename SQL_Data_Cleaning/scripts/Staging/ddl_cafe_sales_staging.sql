/*
 ===============================================================================
 DDL Script: Create cafe_sales_staging Table
 ===============================================================================
 */


-- Drop the table if it exists
DROP TABLE IF EXISTS public.cafe_sales_staging;

-- Create the table
CREATE TABLE public.cafe_sales_staging (
    transaction_id VARCHAR(50),
    item VARCHAR(50),
    quantity VARCHAR(50),
    price_per_unit VARCHAR(50),
    total_spent VARCHAR(50),
    payment_method VARCHAR(50),
    location VARCHAR(50),
    transaction_date VARCHAR(50)
);