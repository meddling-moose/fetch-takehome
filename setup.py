import sqlite3
import pandas as pd

csv_files = {
    "cleaned/users.csv": "users",
    "cleaned/products.csv": "products",
    "cleaned/transactions.csv": "transactions"
}

conn = sqlite3.connect("database.db")

for csv_file, table_name in csv_files.items():
    df = pd.read_csv(csv_file)

    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Loaded {csv_file} into table '{table_name}")

conn.commit()
conn.close()

print("Success!")