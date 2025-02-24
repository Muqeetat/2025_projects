/*
===============================================================================
Stored Procedure: Load Final Layer
===============================================================================
Usage Example:
    
===============================================================================
*/


CREATE OR REPLACE PROCEDURE public.load_final()
LANGUAGE plpgsql
AS $$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
BEGIN
    start_time := now();
    -- Loading cafe_sales_staging table
    RAISE NOTICE '>> Truncating Table: public.cafe_sales';
    TRUNCATE TABLE public.cafe_sales;

    RAISE NOTICE '>> Inserting Data Into: public.cafe_sales';

    INSERT INTO public.cafe_sales(
            transaction_id,
            item,
            quantity,
            price_per_unit,
            total_spent,
            payment_method,
            location,
            transaction_date
        )
    SELECT transaction_id,
        -- Clean item
        CASE
            -- If item is missing, and price_per_unit is Valid ,replace based on price_per_unit
            WHEN (item IS NULL OR item IN ('ERROR', 'UNKNOWN', ''))
                AND (price_per_unit IS NOT NULL AND price_per_unit NOT IN ('ERROR', 'UNKNOWN', ''))
            THEN 
                CASE
                    WHEN CAST(price_per_unit AS FLOAT) = 1.0 THEN 'Cookie'
                    WHEN CAST(price_per_unit AS FLOAT) = 1.5 THEN 'Tea'
                    WHEN CAST(price_per_unit AS FLOAT) = 2.0 THEN 'Coffee'
                    WHEN CAST(price_per_unit AS FLOAT) = 5.0 THEN 'Salad'
                    WHEN CAST(price_per_unit AS FLOAT) = 3.0 THEN 'Cake or Juice'
                    WHEN CAST(price_per_unit AS FLOAT) = 4.0 THEN  'Sandwich or Smoothie'
                    ELSE item
                END
            -- If total_spent and quantity are valid, calculate item based on their ratio
            WHEN (item IS NULL OR item IN ('ERROR', 'UNKNOWN', ''))
                AND (price_per_unit IS NULL OR price_per_unit IN ('ERROR', 'UNKNOWN', ''))
                AND (total_spent IS NOT NULL AND total_spent NOT IN ('ERROR', 'UNKNOWN', ''))
                AND (quantity IS NOT NULL AND quantity NOT IN ('ERROR', 'UNKNOWN', '')) 
            THEN 
                CASE
                    WHEN CAST(total_spent AS FLOAT) / CAST(quantity AS FLOAT) = 1.0 THEN 'Cookie'
                    WHEN CAST(total_spent AS FLOAT) / CAST(quantity AS FLOAT) = 1.5 THEN 'Tea'
                    WHEN CAST(total_spent AS FLOAT) / CAST(quantity AS FLOAT) = 2.0 THEN 'Coffee'
                    WHEN CAST(total_spent AS FLOAT) / CAST(quantity AS FLOAT) = 5.0 THEN 'Salad'
                    WHEN CAST(total_spent AS FLOAT) / CAST(quantity AS FLOAT) = 3.0 THEN 'Cake or Juice'
                    WHEN CAST(total_spent AS FLOAT) / CAST(quantity AS FLOAT) = 4.0 THEN 'Sandwich or Smoothie'
                ELSE item
            END
            -- If total_spent is valid, but quantity and price_per_unit is missing or invalid, default item to Miscellaneous
            WHEN (item IS NULL OR item IN ('ERROR', 'UNKNOWN', ''))
                AND (price_per_unit IS NULL OR price_per_unit IN ('ERROR', 'UNKNOWN', ''))
                AND (total_spent IS NOT NULL AND total_spent NOT IN ('ERROR', 'UNKNOWN', ''))
                AND (quantity IS NULL OR quantity IN ('ERROR', 'UNKNOWN','')) 
            THEN 
                    'Miscellaneous' 
                -- If nothing matches, keep the original item
            ELSE 
                CASE 
                    WHEN item IN ('ERROR', 'UNKNOWN', '') THEN NULL
                    ELSE item
                END
        END AS item,

    -- Clean quantity
        CASE
            -- If quantity is not valid, and price_per_unit and total_spent are Valid, calculate quantity
            WHEN (quantity IS NULL OR quantity IN ('ERROR', 'UNKNOWN', ''))
                AND (price_per_unit IS NOT NULL AND price_per_unit NOT IN ('ERROR', 'UNKNOWN', ''))
                AND (total_spent IS NOT NULL AND total_spent NOT IN ('ERROR', 'UNKNOWN', '')) 
            THEN 
                CAST(CAST(total_spent AS FLOAT) / CAST(price_per_unit AS FLOAT) AS INTEGER)
            
            -- If quantity is not valid , and item is Valid, calculate quantity
            WHEN (quantity IS NULL OR quantity IN ('ERROR', 'UNKNOWN', ''))
                AND (item IS NOT NULL AND item NOT IN ('ERROR', 'UNKNOWN', ''))
                AND (total_spent IS NOT NULL AND total_spent NOT IN ('ERROR', 'UNKNOWN', ''))
            THEN 
                CASE
                    WHEN item = 'Cookie' THEN CAST((CAST(total_spent AS FLOAT) / CAST('1.0' AS FLOAT)) AS INTEGER )
                    WHEN item = 'Tea' THEN CAST((CAST(total_spent AS FLOAT) / CAST('1.5' AS FLOAT)) AS INTEGER )
                    WHEN item = 'Coffee' THEN CAST((CAST(total_spent AS FLOAT) / CAST('2.0' AS FLOAT)) AS INTEGER )
                    WHEN item = 'Cake' THEN CAST((CAST(total_spent AS FLOAT) / CAST('3.0' AS FLOAT)) AS INTEGER )
                    
                    WHEN item = 'Juice' THEN CAST((CAST(total_spent AS FLOAT) / CAST('3.0' AS FLOAT)) AS INTEGER )
                    WHEN item = 'Sandwich' THEN CAST((CAST(total_spent AS FLOAT) / CAST('4.0' AS FLOAT)) AS INTEGER )
                    WHEN item = 'Smoothie' THEN CAST((CAST(total_spent AS FLOAT) / CAST('4.0' AS FLOAT)) AS INTEGER )
                    WHEN item = 'Salad' THEN CAST((CAST(total_spent AS FLOAT) / CAST('5.0' AS FLOAT)) AS INTEGER )
                    ELSE quantity::INTEGER
                END
            -- if quantity and price_per_unit are not valid , and total_spent are 1.0 and 2.0, calculate quantity
            WHEN ( quantity IS NULL OR quantity IN ('ERROR', 'UNKNOWN', ''))
                AND (price_per_unit IS NULL OR price_per_unit IN ('ERROR', 'UNKNOWN', ''))
                AND (total_spent = '1.0') 
            THEN 
                CAST('1' AS INTEGER)
                    
            -- If nothing matches, keep the original item
            ELSE 
                CASE 
                    WHEN quantity IN ('ERROR', 'UNKNOWN', '') THEN NULL
                    ELSE quantity::FLOAT
                END
        END AS quantity,

        -- Clean price_per_unit
        CASE
            -- If price_per_unit is missing, and quantity and total_spent are present, calculate price_per_unit
            WHEN (price_per_unit IS NULL OR price_per_unit IN ('ERROR', 'UNKNOWN', ''))
                AND (quantity IS NOT NULL AND quantity NOT IN ('ERROR', 'UNKNOWN', ''))
                AND (total_spent IS NOT NULL AND total_spent NOT IN ('ERROR', 'UNKNOWN', ''))
                THEN 
                    CAST(total_spent AS FLOAT) / CAST(quantity AS FLOAT)
    
            -- If price_per_unit is missing, and item is valid, calculate price_per_unit
            WHEN (price_per_unit IS NULL OR price_per_unit IN ('ERROR', 'UNKNOWN', ''))
                AND (Item IS NOT NULL AND Item NOT IN ('ERROR', 'UNKNOWN', '')) 
            THEN
                CASE
                    WHEN item = 'Cookie' THEN CAST('1.0' AS FLOAT)
                    WHEN item = 'Tea' THEN CAST('1.5' AS FLOAT)
                    WHEN item = 'Coffee' THEN CAST('2.0' AS FLOAT)
                    WHEN item = 'Cake' THEN CAST('3.0' AS FLOAT)
                    WHEN item = 'Juice' THEN CAST('3.0' AS FLOAT)
                    WHEN item = 'Sandwich' THEN CAST('4.0' AS FLOAT)
                    WHEN item = 'Smoothie' THEN CAST('4.0' AS FLOAT)
                    WHEN item = 'Salad' THEN CAST('5.0' AS FLOAT)
                    ELSE price_per_unit ::FLOAT
                END 
            
        -- if price_per_unit and quantity are missing, and total_spent are 1.0, calculate price_per_unit
            WHEN (quantity IS NULL OR quantity IN ('ERROR', 'UNKNOWN', ''))
                AND (price_per_unit IS NULL OR price_per_unit IN ('ERROR', 'UNKNOWN', ''))
                AND (total_spent IN ('1.0'))
            THEN
                CASE
                    WHEN (CAST(total_spent AS FLOAT)) = 1.0 THEN CAST('1.0' AS FLOAT)
                    ELSE price_per_unit ::FLOAT
                END 
            -- If nothing matches, keep the original item
            ELSE 
                CASE 
                    WHEN price_per_unit IN ('ERROR', 'UNKNOWN', '') THEN NULL
                    ELSE price_per_unit::FLOAT
                END
        END AS price_per_unit,

        -- Clean Total Spent
        CASE   
            -- If total_spent is missing but quantity and price_per_unit are available, calculate it
            WHEN (total_spent IS NULL OR total_spent IN ('ERROR', 'UNKNOWN', '')) 
                AND (quantity IS NOT NULL AND quantity NOT IN ('ERROR', 'UNKNOWN', '')) 
                AND (price_per_unit IS NOT NULL AND price_per_unit NOT IN ('ERROR', 'UNKNOWN', '')) 
            THEN 
                CAST(quantity AS FLOAT) * CAST(price_per_unit AS FLOAT)
            

            -- If total_spent is missing but quantity is available and item name can determine price
            WHEN (total_spent IS NULL OR total_spent IN ('ERROR', 'UNKNOWN', ''))
                AND (price_per_unit IS NULL OR price_per_unit IN ('ERROR', 'UNKNOWN', '')) 
                AND (quantity IS NOT NULL AND quantity NOT IN ('ERROR', 'UNKNOWN', ''))
                AND (item IS NOT NULL AND item NOT IN ('ERROR', 'UNKNOWN', '')) 
            THEN 
                CASE 
                    WHEN item = 'Cookie' THEN CAST(quantity AS FLOAT) * 1.0
                    WHEN item = 'Tea' THEN CAST(quantity AS FLOAT) * 1.5
                    WHEN item = 'Coffee' THEN CAST(quantity AS FLOAT) * 2.0
                    WHEN item = 'Cake' THEN CAST(quantity AS FLOAT) * 3.0
                    WHEN item = 'Juice' THEN CAST(quantity AS FLOAT) * 3.0
                    WHEN item = 'Sandwich' THEN CAST(quantity AS FLOAT) * 4.0
                    WHEN item = 'Smoothie' THEN CAST(quantity AS FLOAT) * 4.0
                    WHEN item = 'Salad' THEN CAST(quantity AS FLOAT) * 5.0
                    ELSE total_spent::FLOAT
                END
            -- If nothing matches, keep the original total_spent but remove invalid values
            ELSE 
                CASE 
                    WHEN total_spent IN ('ERROR', 'UNKNOWN', '') THEN NULL
                    ELSE total_spent::FLOAT
                END
        END AS total_spent,

        -- Clean Payment Method
        CASE
            WHEN payment_method IN ('UNKNOWN', 'ERROR', '') THEN NULL
            ELSE payment_method
        END AS payment_method,

        -- Clean Location
        CASE
            WHEN location IN ('UNKNOWN', 'ERROR', '') THEN NULL
            ELSE location
        END AS location,

        -- Clean Transaction Date
        CASE
            WHEN transaction_date IN ('UNKNOWN', 'ERROR', '') THEN NULL
            ELSE CAST(transaction_date AS DATE)
        END AS transaction_date
    FROM cafe_sales_staging;

    end_time := now();
    RAISE NOTICE '>> Load Duration: % seconds', EXTRACT(EPOCH FROM (end_time - start_time));

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'ERROR OCCURRED: %, SQLSTATE: %', SQLERRM, SQLSTATE;
END;
$$;

-- Call the procedure
CALL public.load_final();