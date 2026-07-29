import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# ---------------- Database Connection ---------------- #

connection_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="Monika@123",      # <-- Apna MySQL Password
    host="localhost",
    port=3306,
    database="customer_intelligence_db",
)

engine = create_engine(connection_url)

# ---------------- Load Data ---------------- #

@st.cache_data
def load_data():
    customers = pd.read_sql("SELECT * FROM customers", engine)
    products = pd.read_sql("SELECT * FROM products", engine)
    orders = pd.read_sql("SELECT * FROM orders", engine)

    sales = (
        orders.merge(customers, on="customer_id", how="inner")
              .merge(products, on="product_id", how="inner")
    )

    return customers, products, orders, sales