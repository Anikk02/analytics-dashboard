import pandas as pd
import random
from faker import Faker
from pathlib import Path

fake = Faker()

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


# CUSTOMER DATA 
customers = []

for i in range(1, 201):
    customers.append([
        i,
        fake.name(),
        fake.email() if random.random() > 0.1 else None,
        random.choice(["North", "South", "East", "West", None]),
        fake.date_between("-2y", "today")
    ])

pd.DataFrame(customers, columns=[
    "customer_id", "name", "email", "region", "signup_date"
]).to_csv(RAW_DIR / "customers.csv", index=False)   # ✅ FIXED


# PRODUCTS
products = [
    [1, "Laptop", "Electronics", 700],
    [2, "Phone", "Electronics", 500],
    [3, "Shoes", "Fashion", 80],
    [4, "Watch", "Accessories", 150],
    [5, "Backpack", "Fashion", 60],
]

pd.DataFrame(products, columns=[
    "product_id", "product_name", "category", "unit_price"
]).to_csv(RAW_DIR / "products.csv", index=False)


#  ORDERS 
statuses = ["completed", "done", "pending", "canceled", "cancelled", "refunded"]

orders = []

for i in range(1, 600):
    orders.append([
        i if random.random() > 0.5 else None,
        random.randint(1, 200) if random.random() > 0.5 else None,
        random.choice(["Laptop", "Phone", "Shoes", "Watch", "Backpack"]),
        random.choice([None, 100, 200, 300, 400, 500]),
        random.choice([
            fake.date(),
            fake.date_time().strftime("%d/%m/%Y"),
            fake.date_time().strftime("%m-%d-%Y")
        ]),
        random.choice(statuses)
    ])

pd.DataFrame(orders, columns=[
    "order_id", "customer_id", "product", "amount", "order_date", "status"
]).to_csv(RAW_DIR / "orders.csv", index=False)