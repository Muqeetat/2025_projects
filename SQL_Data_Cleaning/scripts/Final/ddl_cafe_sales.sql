/*
 ===============================================================================
 DDL Script: Create cafe_sales Table
 ===============================================================================
 */


-- Drop the table if it exists
DROP TABLE IF EXISTS public.cafe_sales;

-- Create the table
CREATE TABLE public.cafe_sales (
    transaction_id VARCHAR(50),
    item VARCHAR(50),
    quantity INT,
    price_per_unit FLOAT,
    total_spent FLOAT,
    payment_method VARCHAR(50),
    location VARCHAR(50),
    transaction_date DATE
); 