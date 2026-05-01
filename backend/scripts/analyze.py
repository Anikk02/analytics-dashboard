import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Load Data

def load_data():

    # ensures pipeline fails early if required files are missing

    try:
        customers = pd.read_csv(PROCESSED_DIR / 'customers_clean.csv')
        orders = pd.read_csv(PROCESSED_DIR / 'orders_clean.csv')
        products = pd.read_csv(RAW_DIR / 'products.csv')

        logger.info("Dataset loaded successfully")

        return customers, orders, products
    
    except FileNotFoundError as e:
        logger.error(f"Missing file: {e}")
        raise

# Merge data

def merge_data(customers, orders, products):

    # Performs left joins to preserve orders history even if:
    # customer is missing or product mapping is missing
    logger.info("Starting data merge")
    
    # Join orders with customers
    orders_customers = orders.merge(
        customers,
        on = 'customer_id',
        how='left'
    )
    
    # Join product metadata ( category, price)
    full_data = orders_customers.merge(
        products,
        left_on='product',
        right_on='product_name',
        how='left'
    )
    
    # track data quality issues after merging
    missing_customers = full_data['customer_id'].isna().sum()
    missing_products = full_data['product_name'].isna().sum()

    logger.info(
        f"Merge completed | missing_customers={missing_customers},"
        f"missing_products={missing_products}"
    )

    return full_data

## MONTHLY REVENUE

def monthly_revenue(df):

    # We compute total revenue per month only after completed orders
    logger.info("Computing monthly revenue")

    # filter only successful transactions
    data = df[df['status']=='completed']
    
    # Group by time period (YYYY-MM)
    result = data.groupby('order_year_month')['amount'].sum().reset_index()
    result.columns = ['order_year_month', 'total_revenue']

    result.to_csv(PROCESSED_DIR / 'monthly_revenue.csv', index=False)

    logger.info('monthly_revenue.csv is saved')

    return result

## TOP CUSTOMERS

def top_customers(df):
    logger.info('Computing top customers')
    
    # Only completed orders contribute to revenue
    data = df[df['status']=='completed']
    
    # Aggregate spending per customer
    result = data.groupby(
        ['customer_id', 'name', 'region']
    )['amount'].sum().reset_index()

    result.rename(columns={'amount': 'total_spend'}, inplace=True)
    
    #filtering top 10 customers
    result = result.sort_values('total_spend',ascending=False).head(10)

    result.to_csv(PROCESSED_DIR / 'top_customers.csv', index=False)

    logger.info("top_customers.csv is saved successfully")

    return result

## Category Performance

def category_performance(df):
    # analyze revenue contribution per product category

    logger.info("Computing category performed..")

    data = df[df['status']=='completed']

    result = data.groupby('category').agg(
        total_revenue=('amount', 'sum'),
        avg_order_value=('amount','mean'),
        orders=('order_id','count')
    ).reset_index()

    result.to_csv(PROCESSED_DIR / 'category_performance.csv', index=False)

    logger.info("category_performance.csv is saved")

    return result

## REGIONAL ANALYSIS

def regional_analysis(df):
    # Measures performance across different geographic regions.

    logger.info("Computing regional analysis..")

    # filter completed transactions
    data = df[df["status"] == "completed"]

    result = data.groupby("region").agg(
        customers=("customer_id", "nunique"),
        orders=("order_id", "count"),
        revenue=("amount", "sum")
    ).reset_index()

    # Derived KPI: revenue per customer
    result["avg_revenue_per_customer"] = (
        result["revenue"] / result["customers"]
    )

    result.to_csv(PROCESSED_DIR / "regional_analysis.csv", index=False)

    logger.info("regional_analysis.csv saved successfully")

    return result

# Churn Detection

def add_churn_flag(df, top_customers_df):
    # Flags customers who have NOT made any completed purchase in the last 90 days

    logger.info("Calculating churn flag")

    # 🔒 Ensure datetime
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    # Find latest valid transaction date
    latest_date = df["order_date"].max()

    if pd.isna(latest_date):
        logger.error("No valid order_date found for churn calculation")
        raise ValueError("Invalid order_date data")

    # Define churn threshold window
    cutoff = latest_date - pd.Timedelta(days=90)

    # Filter recent active customers (safe datetime comparison)
    recent_orders = df[
        (df["status"].astype(str).str.lower() == "completed") &
        (df["order_date"] >= cutoff)
    ]

    active_customers = set(recent_orders["customer_id"].dropna())

    # Mark churn status in top customers table
    top_customers_df["churned"] = ~top_customers_df["customer_id"].isin(active_customers)

    top_customers_df.to_csv(PROCESSED_DIR / "top_customers.csv", index=False)

    logger.info("Churn flag updated in top_customers.csv")

    return top_customers_df

# Pipeline execution

def main():
    #Orchestrates the full analytics pipeline

    # load -> merge -> analyze -> export outputs

    logger.info('Starting analysis pipeline')

    customers, orders, products = load_data()

    full_data = merge_data(customers, orders, products)

    monthly_revenue(full_data)
    top = top_customers(full_data)
    category_performance(full_data)
    regional_analysis(full_data)

    top = add_churn_flag(full_data, top)

    logger.info('Analysis pipeline completed successfully')

if __name__ == '__main__':
    main()
                            
