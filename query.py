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

result = pd.read_sql(top_five_brands_by_receipt, conn)
print(result)

# Second Closed-Ended Query
top_five_brands_by_sales = """

"""

conn.close()