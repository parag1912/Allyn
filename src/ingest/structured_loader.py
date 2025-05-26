import duckdb
import pandas as pd

# Load CSV files
customers_df = pd.read_csv("data/structured/customer.csv")
orders_df = pd.read_csv("data/structured/order.csv")
emissions_df = pd.read_csv("data/structured/emissions.csv")

# Connect to persistent DuckDB file
con = duckdb.connect("allyin.duckdb")

# Drop existing tables if they exist
con.execute("DROP TABLE IF EXISTS customers")
con.execute("DROP TABLE IF EXISTS orders")
con.execute("DROP TABLE IF EXISTS emissions")

# Register and save tables
con.register("customers_df", customers_df)
con.register("orders_df", orders_df)
con.register("emissions_df", emissions_df)

con.execute("CREATE TABLE customers AS SELECT * FROM customers_df")
con.execute("CREATE TABLE orders AS SELECT * FROM orders_df")
con.execute("CREATE TABLE emissions AS SELECT * FROM emissions_df")

# Optional: check
print(con.sql("SELECT * FROM customers LIMIT 5").df())
print("✅ Tables saved to allyin.duckdb")
