# ================================================
# 🐍 Foodr Analysis Tutorial with Pandas & NumPy
# ================================================

# ▶️ Required Libraries

import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine

# ▶️ Step 1: Connect to PostgreSQL (update with your credentials)
db_user = "postgres"
db_pass = "admin"
db_host = "localhost"
db_port = "5432"
db_name = "Foodr"

engine = create_engine(f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")
print("✅ Connected to the database successfully!")

# ▶️ Step 2: Load tables into Pandas DataFrames
meals_df = pd.read_sql("SELECT* FROM meals", engine)
orders_df = pd.read_sql("SELECT * FROM orders", engine)
stock_df = pd.read_sql("SELECT * FROM stock", engine)
print("\nSample meals data:")
print(meals_df.head())
print("\nSample orders data:")
print(orders_df.head())
print("\nSample stock data:")
print(stock_df.head())

# ✅ Task 1: How many unique meals and eateries exist?
print("\n✅ Task 1: Unique counts")
print("Unique meals:", meals_df["meal_id"].nunique())
print("Unique eateries:",meals_df["eatery"].nunique())

# ▶️ Step 3: Total revenue per meal
orders_df["order_revenue"] = orders_df["order_quantity"] * orders_df["meal_id"].map(
    meals_df.set_index("meal_id")["meal_price"]
)
revenue_per_meal = orders_df.groupby("meal_id")["order_revenue"].sum().reset_index()

revenue_per_meal = revenue_per_meal.merge(meals_df[["meal_id", "eatery"]], on="meal_id", how="left")
print("\n✅Task2: Top 5 revenue-generating meals:")
print(revenue_per_meal.sort_values(by="order_revenue", ascending=False).head())

# ▶️ Step 4: Profit per meal
meals_df["profit_margin"] = meals_df["meal_price"]-meals_df["meal_cost"]
orders_df["meal_cost"] = orders_df["meal_id"].map(meals_df.set_index("meal_id")["meal_cost"])
orders_df["meal_price"] = orders_df["meal_id"].map(meals_df.set_index("meal_id")["meal_price"])
orders_df["total_cost"] = orders_df["order_quantity"]*orders_df["meal_cost"]
orders_df["total_price"] = orders_df["order_quantity"]*orders_df["meal_price"]
orders_df["profit"] = orders_df["total_price"]-orders_df["total_cost"]
profit_by_eatery = orders_df.merge(meals_df[["meal_id", "eatery"]], on="meal_id", how="left")\
    \
.groupby("eatery")["profit"].sum().sort_values(ascending=False).reset_index()
print("\n✅Task 3: Total profit by eatery:")
print(profit_by_eatery)

# ▶️ Step 5: Analyze stock levels vs orders
stocked = stock_df.groupby("meal_id")["stocked_quantity"].sum()
ordered = orders_df.groupby("meal_id")["order_quantity"].sum()
stock_vs_orders = pd.DataFrame({
    "stocked": stocked,
    "ordered": ordered
}).fillna(0)
stock_vs_orders["leftover"] = stock_vs_orders["stocked"] - stock_vs_orders["ordered"]
print("\n✅Task 4: Meals with negative leftover stock (oversold):" )
print(stock_vs_orders[stock_vs_orders["leftover"]<0])

# ▶️ Step 6: Daily revenue trend using NumPy
daily_revenue = orders_df.groupby("order_date")["total_price"].sum().reset_index()
daily_revenue["7_day_avg"] = daily_revenue["total_price"].rolling(window=7).mean()
print("\n✅Task 5: Revenue trend (last 10 days):")
print(daily_revenue.tail(10))
print("✅ You’ve completed the Foodr Data Analysis Exercise!")

# sp100_analysis_numpy.py

import numpy as np
import matplotlib.pyplot as plt
import csv
