
SELECT *
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'cafe_sales';


/*
Dimensions Exploration

Identify the unique values (or categories) for each dimension

Dimensions: Transaction_id, item, payment_method, location,transaction_date
*/

-- find the unique items
SELECT DISTINCT item
FROM cafe_sales
ORDER BY item;

-- find the unique payment methods
SELECT DISTINCT payment_method
FROM cafe_sales
ORDER BY payment_method;

-- find the unique locations
SELECT DISTINCT location
FROM cafe_sales
ORDER BY location;

/*
Date Exploration

Identify the earliest and latest dates (boundaries)

Understand the scope of data and the timespan
*/

-- Find the earliest and latest transaction dates
SELECT MIN(transaction_date) AS first_transaction_date,
	   MAX(transaction_date) AS last_transaction_date
FROM cafe_sales

/*
Measures Exploration

Calculate the key metric of the business (Big Numbers)

*/

-- Null values in the dataset

SELECT '0' AS no, 'Transaction ID' AS column_name, COUNT(*) AS null_count FROM cafe_sales WHERE transaction_id IS NULL
UNION ALL
SELECT '1','Item', COUNT(*) FROM cafe_sales WHERE item IS NULL
UNION ALL
SELECT '2','Quantity', COUNT(*) FROM cafe_sales WHERE quantity IS NULL
UNION ALL
SELECT '3','Price Per Unit', COUNT(*) FROM cafe_sales WHERE price_per_unit IS NULL
UNION ALL
SELECT '4','Total Spent', COUNT(*) FROM cafe_sales WHERE total_spent IS NULL
UNION ALL
SELECT '5','Payment Method', COUNT(*) FROM cafe_sales WHERE payment_method IS NULL
UNION ALL
SELECT '6','Location', COUNT(*) FROM cafe_sales WHERE location IS NULL
UNION ALL
SELECT '7','Transaction Date', COUNT(*) FROM cafe_sales WHERE transaction_date IS NULL;

--Findings: All columns have null values except for the transaction_id column.


-- Generate a summary of the all the key metrics

SELECT 'Total Sales' AS measure_name, SUM(total_spent) AS measure_value FROM cafe_sales
UNION ALL
SELECT 'Total Items Sold', SUM(quantity) FROM cafe_sales
UNION ALL
SELECT 'Average Price', ROUND(AVG(price_per_unit), 2) FROM cafe_sales
UNION ALL
SELECT 'Total No Transactions', COUNT(DISTINCT transaction_id) FROM cafe_sales
UNION ALL
SELECT 'Total No Items', COUNT(DISTINCT item) FROM cafe_sales

-- Findings: The total sales amount to 89,096, total items sold is 30,180, average price is 2.95, 
-- total number of transactions is 10,000, and total number of items is 9.

-- ### **Item & Sales Analysis**  
-- Find the highest selling item by quantity 
SELECT item, SUM(quantity) AS total_quantity_sold
FROM cafe_sales
GROUP BY item
ORDER BY total_quantity_sold DESC
LIMIT 1;

--Findings: The highest selling item by quantity is Coffee with 3,904 units sold.

-- Find the least selling item by quantity
SELECT item, SUM(quantity) AS total_quantity_sold
FROM cafe_sales
WHERE (item IS NOT NULL AND item != 'Miscellaneous')
GROUP BY item
ORDER BY total_quantity_sold ASC
LIMIT 4;

-- Findings: The least sold items by quantity are likely Smoothie or Sandwich, 
-- as their sales figures are consistently lower than those of 'Cake or Juice'. 
-- Additionally, Smoothie and Sandwich rank third and fourth in total quantity sold.

-- Find the top 5 highest revenue-generating items
SELECT item, SUM(total_spent) AS total_revenue
FROM cafe_sales
WHERE item IS NOT NULL
GROUP BY item
ORDER BY total_revenue DESC
LIMIT 5;

-- Findings: The top 5 highest revenue-generating items are Salad, Sandwich, Smoothie, Juice, and Cake.

-- ### **Transaction & Payment Analysis**  
-- 9. Find the most used payment method
SELECT payment_method, COUNT(*) FROm cafe_sales
GROUP BY payment_method
ORDER BY COUNT(*) DESC
LIMIT 1;

-- Findings: The most used payment method is 'Null' with count 3,178.

-- Find the average transaction amount for each payment method
SELECT payment_method, AVG(total_spent) AS average_transaction_amount
FROM cafe_sales
GROUP BY payment_method
ORDER BY average_transaction_amount DESC;

-- Find the highest total revenue by payment method  
SELECT payment_method, SUM(total_spent) AS total_revenue
FROM cafe_sales
GROUP BY payment_method
ORDER BY total_revenue DESC
LIMIT 1;

-- Findings: the highest total revenue by payment method is 'Null' with a total revenue of 27,813.5   

-- ### **Location-Based Analysis**  
--  Which location has the highest total sales (`total_spent`)? 
SELECT location, SUM(total_spent) AS total_sales
FROM cafe_sales
GROUP BY location
ORDER BY total_sales DESC
LIMIT 1; 

-- Findings: the location with the highest total sales is 'Null' with total sales of 35,369.5

-- What is the most popular item sold in each location? 
SELECT location, item, SUM(quantity) AS total_quantity_sold
FROM cafe_sales
WHERE location IS NOT NULL AND item IS NOT NULL AND quantity IS NOT NULL
GROUP BY location, item
ORDER BY total_quantity_sold DESC
LIMIT 1; 


-- Which location has the highest average transaction value?
SELECT location, AVG(total_spent) AS average_transaction_value
FROM cafe_sales
GROUP BY location
ORDER BY average_transaction_value DESC
LIMIT 1;


-- ### **Time-Based Analysis**
-- What is the total sales daily?  
SELECT transaction_date, SUM(total_spent) AS total_sales
FROM cafe_sales
GROUP BY transaction_date
ORDER BY transaction_date;

-- On which date was the highest revenue generated? 
SELECT transaction_date, SUM(total_spent) AS total_sales
FROM cafe_sales
GROUP BY transaction_date
ORDER BY total_sales DESC

-- What are the peak sales days (days with the highest number of transactions)?  
SELECT transaction_date, COUNT(DISTINCT transaction_id) AS total_transactions
FROM cafe_sales
GROUP BY transaction_date
ORDER BY total_transactions DESC


-- Which month has the highest total revenue?
SELECT EXTRACT(MONTH FROM transaction_date) AS month, SUM(total_spent) AS total_revenue
FROM cafe_sales
GROUP BY month
ORDER BY total_revenue DESC
LIMIT 1;

-- Finding: The month with the highest total revenue is month 6 with a total revenue of 7,353.


/*
Findings Summary:

The analysis reveals that all columns contain null values except for the transaction_id column, which may affect the reliability of some findings.
The total sales amount to $89,096, with 30,180 items sold across 10,000 transactions.
The average price per item is $2.95, and there are a total of 9 unique items in the dataset.
Among these, Coffee is the highest-selling item by quantity, with 3,904 units sold, while Smoothie and Sandwich might have the lowest sales figures,
ranking third and fourth in total quantity sold, below 'smoothie or sandwich' item. 
In terms of revenue, the top five highest-earning items are Salad, Sandwich, Smoothie, Juice, and Cake.

For payment methods, the most frequently recorded method is 'Null' with 3,178 transactions, indicating a significant amount of missing or unclassified payment data. 
This raises concerns about data completeness and accuracy. Additionally, the month with the highest revenue is June (Month 6), generating $7,353 in total sales.

In conclusion, while the dataset provides valuable insights into sales performance, the high number of null values affects the reliability of some findings. 
Key metrics such as the most used payment method may not accurately reflect actual payment trends. 
Future analyses should focus on addressing missing data to improve the accuracy of insights and decision-making.
*/











