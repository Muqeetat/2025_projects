SELECT COUNT(*) total_rows
FROM cafe_sales_staging

--=====================================================
--- transcation_id column
--=====================================================

-- Check For Nulls or Duplicates in Primary Key
-- Expectation: No Result

SELECT transaction_id, COUNT(*)
FROM cafe_sales_staging
GROUP BY transaction_id
HAVING COUNT(*) > 1 OR transaction_id IS NULL

SELECT DISTINCT transaction_id
FROM cafe_sales_staging
ORDER BY transaction_id;

SELECT transaction_id
FROM cafe_sales_staging
WHERE transaction_id IN ('UNKNOWN','ERROR',' ')

SELECT transaction_id
FROM cafe_sales_staging
WHERE transaction_id LIKE '%-%'

-- Check if total no of rows is equal to the no of distinct transaction_id
SELECT COUNT (DISTINCT transaction_id)
FROM cafe_sales_staging

-- Check for unwanted Spaces
SELECT transaction_id
FROM cafe_sales_staging
WHERE transaction_id != TRIM(transaction_id)

-- =====================================================
-- item column 
-- =====================================================

-- Check For Nulls
-- Expectation: No Result

SELECT COUNT(*)
FROM cafe_sales_staging
WHERE item IS NULL

-- Check for unwanted Spaces
SELECT item
FROM cafe_sales_staging
WHERE item != TRIM(item)

SELECT COUNT(*)
FROM cafe_sales_staging
WHERE item IN ('UNKNOWN','ERROR','')

SELECT DISTINCT item
FROM cafe_sales_staging

SELECT DISTINCT item, price_per_unit
FROM cafe_sales_staging
ORDER BY price_per_unit, item

SELECT DISTINCT item, price_per_unit,quantity,total_spent
FROM cafe_sales_staging
WHERE item in ('UNKNOWN','ERROR', '') AND price_per_unit IS NULL
ORDER BY price_per_unit, item

SELECT *
FROM cafe_sales_staging
WHERE item in ('UNKNOWN','ERROR','') OR item IS NULL
ORDER BY price_per_unit, item

-- =====================================================
-- quantity Column
-- =====================================================

SELECT *
FROM cafe_sales_staging
WHERE quantity in ('UNKNOWN','ERROR','') OR quantity IS NULL

SELECT DISTINCT quantity
FROM cafe_sales_staging

-- =====================================================
-- price_per_unit Column
-- =====================================================

SELECT DISTINCT price_per_unit
FROM cafe_sales_staging
ORDER BY price_per_unit

SELECT *
FROM cafe_sales_staging
WHERE price_per_unit in ('UNKNOWN','ERROR','') OR price_per_unit IS NULL

-- =====================================================
-- total_spent Column
-- =====================================================

SELECT DISTINCT total_spent
FROM cafe_sales_staging

SELECT DISTINCT quantity, price_per_unit, total_spent
FROM cafe_sales_staging
WHERE total_spent in ('UNKNOWN','ERROR','') OR total_spent IS NULL

-- =====================================================
-- payment_method column
-- =====================================================

-- Check for unwanted Spaces
SELECT payment_method
FROM cafe_sales_staging
WHERE payment_method != TRIM(payment_method)

SELECT DISTINCT payment_method
FROM cafe_sales_staging

-- =====================================================
-- location Column
-- =====================================================

-- Check for unwanted Spaces
SELECT location
FROM cafe_sales_staging
WHERE location != TRIM(location)

SELECT DISTINCT location
FROM cafe_sales_staging

-- =====================================================
-- transaction_date column
-- =====================================================

SELECT *
FROM cafe_sales_staging
WHERE transaction_date in ('UNKNOWN','ERROR',' ') OR transaction_date IS NULL
