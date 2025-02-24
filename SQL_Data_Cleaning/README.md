# Data Cleansing Using SQL

This document explains how I cleaned the dataset using SQL.

## Dataset Information

- **Dataset Link:** [Cafe Sales Dirty Dataset](https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training/data)
- **Notion Link:** [Dataset Cleaning Project](https://destiny-babcat-d2e.notion.site/Dataset-Cleaning-Project-19b747e5d0ef8009aeedc90339302703)

## Tables Used

- **cafe_sales** - The table with clean data.
- **cafe_sales_staging** - The table to stage the data before cleaning.

## Stored Procedures

- **load_staging** - Performs a bulk insert of data into the staging table.
- **load_final** - Executes the process to populate the `cafe_sales` table from `cafe_sales_staging`.

## Steps Taken

### 1. Cleaning the Item Column

- If an item was missing or had an error, I used the price per unit to determine the correct item.
- If the price was also missing, I used the total spent and quantity to find the item.
- If none of the above worked, I set the item as 'Miscellaneous'.

### 2. Cleaning the Quantity Column

- If quantity was missing but price per unit and total spent were available, I calculated quantity as `total_spent / price_per_unit`.
- If quantity was missing but the item name was valid, I used known prices to determine quantity.
- If all else failed, I kept the original quantity if valid.

### 3. Cleaning the Price per Unit Column

- If price per unit was missing but quantity and total spent were available, I calculated it as `total_spent / quantity`.
- If only the item name was valid, I used standard prices for each item.
- If none of these worked, I kept the original price if valid.

### 4. Cleaning the Total Spent Column

- If total spent was missing but price per unit and quantity were available, I calculated it as `price_per_unit * quantity`.
- If only the item name and quantity were valid, I used standard prices to find total spent.
- If nothing worked, I kept the original total spent if valid.

### 5. Cleaning Other Columns

- **Payment Method, Location, and Transaction Date:**
  - If values were 'UNKNOWN' or 'ERROR', I set them to NULL.
  - Otherwise, I kept the original values.

## Data Quality Checks

To ensure data accuracy, I ran the following SQL checks:

### E.g Checking for Unwanted Spaces in Location Column

```sql
SELECT location
FROM cafe_sales_staging
WHERE location != TRIM(location);
```
