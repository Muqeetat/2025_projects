# **SQL Exploratory Data Analysis (EDA) Project**  

## **Overview**  

This project continues my **SQL Data Cleaning Project**, focusing on **Exploratory Data Analysis (EDA)** to uncover insights, trends, and patterns from the cleaned dataset.  

## **Objectives**  

- Analyze sales trends, item performance, and payment behaviors.  
- Identify top-selling items and revenue distribution.  
- Assess time-based sales patterns and data limitations.  

## **Dataset**  

- **Columns:** `transaction_id, item, quantity, price_per_unit, total_spent, payment_method, location, transaction_date`.  
- **Key Issue:** Presence of null values in key columns.  

## **Key Findings**  

- **Data Quality:** All columns contain null values except for `transaction_id`, which may affect data reliability.  
- **Sales Overview:**  
  - **Total Revenue:** `$89,096`  
  - **Total Items Sold:** `30,180`  
  - **Average Price per Item:** `$2.95`  
  - **Total Transactions:** `10,000`  
  - **Total Unique Items:** `9`  
- **Item Performance:**  
  - **Most Sold Item:** `Coffee (3,904 units sold)`  
  - **Top Revenue-Generating Items:** `Salad, Sandwich and Smoothie`  
- **Payment Insights:**  
  - **Most Used Payment Method:** `'Null' (3,178 transactions)`, indicating missing or unclassified data.  
- **Time-Based Insights:**  
  - **Peak Sales Month:** `June (Month 6)`, generating `$7,353` in total sales.  

## **SQL Techniques**  

- Aggregations (`SUM, AVG, COUNT`), grouping (`GROUP BY`), and time-based analysis (`DATE` functions).  

## **Conclusion**  

While this analysis provides valuable insights into sales performance, the presence of null values affects the reliability of some findings, such as payment method distribution.
