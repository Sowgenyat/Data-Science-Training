import mysql.connector
import pandas as pd
import numpy as np
import os

# Database connection
conn = mysql.connector.connect(
    host='127.0.0.1',
    port=3305,
    user='root',
    password='9976565139@Sow',
    database='retail_sales'
)
print("Database connection successful")

# Query with joins
query = """
SELECT s.sale_id, s.sale_date, s.quantity, 
       p.name AS product_name, p.category, p.price, p.cost,
       st.name AS store_name, st.region,
       e.name AS employee_name, e.role
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN stores st ON s.store_id = st.store_id
JOIN employees e ON s.emp_id = e.emp_id;
"""

df = pd.read_sql(query, conn)

# Add calculated fields
df['revenue'] = df['quantity'] * df['price']
df['profit'] = df['revenue'] - (df['quantity'] * df['cost'])
df['profit_margin'] = (df['profit'] / df['revenue']) * 100

# Check categories present
print("Categories found in data:", df['category'].unique())
print("Number of rows:", len(df))

# Always overwrite the file safely
csv_path = "cleaned_sales_data.csv"

# If file exists, remove it first to avoid permission issues
if os.path.exists(csv_path):
    os.remove(csv_path)

df.to_csv(csv_path, index=False)
print(f"Cleaned sales data saved to: {os.path.abspath(csv_path)}")

conn.close()
