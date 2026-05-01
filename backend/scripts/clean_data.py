import pandas as pd
import numpy as np
import warnings
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def load_csv(file_name: str) -> pd.DataFrame:
    path = RAW_DIR / file_name
    if not path.exists():
        logger.error(f"{file_name} not found in raw data folder") 
        raise FileNotFoundError(f"{file_name} not found in raw data folder")
    
    try:
        df = pd.read_csv(path)
    except Exception as e:
        logger.error(f"Failed to read {file_name}: {e}")
    
    if df.empty:
        logger.warning(f'{file_name} is empty')
    
    logger.info(f"Loaded file: {file_name} | shape: {df.shape}")

    return df


def parse_data(val):
    # Handles multiple date formats safely
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"):
        try:
            return pd.to_datetime(val, format=fmt)
        except Exception:
            continue
    return pd.NaT


# Clean customer data

def clean_customers(df: pd.DataFrame) -> pd.DataFrame:

    before_rows = len(df)

    df = df.sort_values('signup_date').drop_duplicates(
        subset=['customer_id'], keep='last'
    )

    df['email'] = df['email'].str.lower()

    df['is_valid_email'] = df['email'].apply(
        lambda x: isinstance(x, str) and '@' in x and '.' in x
    )

    df['signup_date'] = pd.to_datetime(df['signup_date'], errors='coerce')

    missing_dates = df['signup_date'].isna().sum()

    if missing_dates > 0:
        logger.warning(f"{missing_dates} signup_date values could not be parsed")

    df['name'] = df['name'].str.strip()
    df['region'] = df['region'].astype(str).str.strip()
    df['region'] = df['region'].replace('nan', np.nan).fillna('Unknown')

    logger.info(f"Customers cleaned: before={before_rows}, after={len(df)}")

    return df

## Clean orders data

def clean_orders(df: pd.DataFrame) -> pd.DataFrame:

    before_rows = len(df)

    df = df.dropna(subset=['order_id','customer_id'], how='all')

    df['order_date'] = df['order_date'].apply(parse_data)

    df['amount'] = df['amount'].fillna(
        df.groupby('product')['amount'].transform('median')
    )

    df['status'] = df['status'].str.lower().replace({
        'done': 'completed',
        'canceled': 'cancelled',
        'cancelled': 'cancelled'
    })

    df['status'] = df['status'].apply(
        lambda x: x if x in ['completed','pending','cancelled','refunded'] else 'pending'
    )

    df['order_year_month'] = df['order_date'].dt.strftime("%Y-%m")

    logger.info(f"Orders cleaned: before={before_rows}, after={len(df)}")

    return df

# main function
def main():

    logger.info('Starting data cleaning pipeline')

    customers = load_csv('customers.csv')
    orders = load_csv('orders.csv')

    customers_clean = clean_customers(customers)
    orders_clean = clean_orders(orders)

    customers_clean.to_csv(PROCESSED_DIR / 'customers_clean.csv', index=False)
    orders_clean.to_csv(PROCESSED_DIR / 'orders_clean.csv', index=False)

    logger.info('Cleaned files saved to data/processed/')
    logger.info('Data cleaning pipeline completed successfully')

if __name__ == "__main__":
    main()

