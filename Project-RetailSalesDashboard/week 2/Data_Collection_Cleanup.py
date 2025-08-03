import mysql.connector
import pandas as pd
import numpy as np

conn = mysql.connector.connect(
    host='127.0.0.1',
    port=3305,
    user='root',
    password='9976565139@Sow',
    database='retail_sales'
)
print("Database connection succesfull")
query = """
select s.sale_id, s.sale_date, s.quantity, 
       p.name AS product_name, p.category, p.price, p.cost,
       st.name AS store_name, st.region,
       e.name AS employee_name, e.role
from sales s
join products p ON s.product_id = p.product_id
join stores st ON s.store_id = st.store_id
join employees e ON s.emp_id = e.emp_id;
"""
df = pd.read_sql(query, conn)
df['revenue'] = df['quantity'] * df['price']
df['profit'] = df['revenue'] - (df['quantity'] * df['cost'])
df['profit_margin'] = (df['profit'] / df['revenue']) * 100
summary = df.groupby('store_name')[['revenue', 'profit']].sum().reset_index()
print("Cleaned Data:")
print(df.head())
print("\nRevenue & Profit by Store:")
print(summary)
df.to_csv("cleaned_sales_data.csv", index=False)
conn.close()