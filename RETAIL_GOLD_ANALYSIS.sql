-- Database and Schema Setup
USE DATABASE RETAIL_DW;
USE SCHEMA GOLD;

-- 1. High-Level Metric Summary
SELECT 
    COUNT(*) AS total_rows,
    COUNT(DISTINCT store_id) AS total_stores,
    MIN(trade_date) AS min_date,
    MAX(trade_date) AS max_date,
    SUM(footfall) AS total_footfall,
    SUM(bills) AS total_bills,
    ROUND(SUM(revenue), 2) AS grand_total_revenue
FROM RETAIL_DW.GOLD.GOLD_STORE_HOUR;

-- 2. Store Performance Ranking
SELECT 
    store_id,
    city,
    format,
    SUM(footfall) AS total_footfall,
    SUM(bills) AS total_bills,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(conversion_rate), 4) AS avg_conversion_rate
FROM RETAIL_DW.GOLD.GOLD_STORE_HOUR
GROUP BY store_id, city, format
ORDER BY total_revenue DESC;

-- 3. Hourly Trend Analysis (Optimized for Categorical Bar Charts)
SELECT 
    LPAD(hour::VARCHAR, 2, '0') || ':00' AS store_hour,
    SUM(footfall) AS total_footfall,
    SUM(bills) AS total_bills,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM RETAIL_DW.GOLD.GOLD_STORE_HOUR
GROUP BY hour
ORDER BY hour ASC;
