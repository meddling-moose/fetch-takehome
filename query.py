import sqlite3
import pandas as pd

conn = sqlite3.connect("database.db")

# First Closed-Ended Query
top_five_brands_by_receipt = """
           SELECT p.BRAND,
                  COUNT(t.receipt_ID) AS receipt_count
           FROM users u
           JOIN transactions t ON u.ID = t.USER_ID
           JOIN products p ON t.BARCODE = p.BARCODE
           WHERE DATE('now') >= DATE(u.BIRTH_DATE, '+21 years')
           GROUP BY p.Brand
           ORDER BY receipt_count DESC
           LIMIT 5
"""

result1 = pd.read_sql(top_five_brands_by_receipt, conn)
print(result1)

# Second Closed-Ended Query
top_five_brands_by_sales = """
    SELECT p.BRAND,
           SUM(t.FINAL_SALE) as total_sales
    FROM users u
    JOIN transactions t ON u.ID = t.USER_ID
    JOIN products p ON t.BARCODE = p.BARCODE
    WHERE DATE('now') >= DATE(u.CREATED_DATE, '+6 months')
    GROUP BY p.BRAND
    ORDER BY total_sales DESC
    LIMIT 5
"""

result2 = pd.read_sql(top_five_brands_by_sales, conn)
print(result2)

# Thrird Query
chips_and_salsa = """
    SELECT p.BRAND,
           SUM(t.FINAL_SALE) as total_sales
    FROM products p
    JOIN transactions t ON p.BARCODE = t.BARCODE
    WHERE p.CATEGORY_2 = 'Dips & Salsa' -- Category 2 is the only on that has Chips and Salsa
    GROUP BY p.BRAND
    ORDER BY total_sales DESC
    LIMIT 1
"""

result3 = pd.read_sql(chips_and_salsa, conn)
print(result3)

generation_sales = """
    WITH generation_sales AS (
        SELECT 
            CASE 
                WHEN u.BIRTH_DATE BETWEEN DATE('1965-01-01') AND DATE('1980-12-31') THEN 'Generation X'
                WHEN u.BIRTH_DATE BETWEEN DATE('1981-01-01') AND DATE('1996-12-31') THEN 'Millennials'
                WHEN u.BIRTH_DATE BETWEEN DATE('1997-01-01') AND DATE('2012-12-31') THEN 'Generation Z'
                WHEN u.BIRTH_DATE <= DATE('1964-12-31') THEN 'Baby Boomers'
                ELSE 'Unknown'
            END AS generation,
            SUM(t.FINAL_SALE) AS total_sales
        FROM users u
        JOIN transactions t ON u.ID = t.USER_ID
        JOIN products p ON t.BARCODE = p.BARCODE
        WHERE p.CATEGORY_1 = 'Health & Wellness'
        GROUP BY generation
    ),
    total_health_wellness_sales AS (
        SELECT SUM(t.FINAL_SALE) AS total_sales
        FROM transactions t
        JOIN products p ON t.BARCODE = p.BARCODE
        WHERE p.CATEGORY_1 = 'Health & Wellness'  -- Total sales in Health & Wellness
    )
    SELECT g.generation,
           g.total_sales,
           (g.total_sales * 100.0 / t.total_sales) AS percentage_of_health_wellness_sales
    FROM generation_sales g
    CROSS JOIN total_health_wellness_sales t
    ORDER BY percentage_of_health_wellness_sales DESC
"""

result4 = pd.read_sql(generation_sales, conn)
print(result4)

conn.close()