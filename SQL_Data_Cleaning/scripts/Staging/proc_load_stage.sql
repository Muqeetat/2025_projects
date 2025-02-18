/*
===============================================================================
Stored Procedure: Load Staging Layer
===============================================================================
Usage Example:
    
===============================================================================
*/


CREATE OR REPLACE PROCEDURE public.load_staging()
LANGUAGE plpgsql
AS $$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
BEGIN
    -- Loading cafe_sales_staging table
    RAISE NOTICE '>> Truncating Table: public.cafe_sales_staging';
    TRUNCATE TABLE public.cafe_sales_staging;

    RAISE NOTICE '>> Inserting Data Into: public.cafe_sales_staging';
    start_time := now();

    COPY public.cafe_sales_staging
    FROM 'C:\Users\DELL\Desktop\2025_projects\SQL_Data_Cleaning\datasets\dirty_cafe_sales.csv' 
    DELIMITER ',' CSV HEADER;

    end_time := now();
    RAISE NOTICE '>> Load Duration: % seconds', EXTRACT(EPOCH FROM (end_time - start_time));

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'ERROR OCCURRED: %, SQLSTATE: %', SQLERRM, SQLSTATE;
END;
$$;

-- Call the procedure
CALL public.load_staging();
