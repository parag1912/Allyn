# Code to load structured CSVs into DuckDB
import duckdb
import pandas as pd

# Load CSV files
customers = pd.read_csv("data/structured/customer.csv")
orders = pd.read_csv("data/structured/order.csv")
emissions = pd.read_csv("data/structured/emissions.csv")

# Register DataFrames as DuckDB tables
duckdb.sql("CREATE TABLE customers AS SELECT * FROM customers")
duckdb.sql("CREATE TABLE orders AS SELECT * FROM orders")
duckdb.sql("CREATE TABLE emissions AS SELECT * FROM emissions")

# Sample query
print(duckdb.sql("SELECT * FROM customers LIMIT 10").df())
