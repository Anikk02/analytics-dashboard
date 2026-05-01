from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import pandas as pd
import logging

# APP SETUP

app = FastAPI(title="Analytics Dashboard API")

logger = logging.getLogger(__name__)

#Enable CORS (for Frontend Access)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data' / 'processed'

# Utility Loader

def load_csv(file_name: str):
    path = DATA_DIR / file_name

    if not path.exists():
        raise HTTPException(status_code=404, detail=f"{file_name} not found")
    
    return pd.read_csv(path)

#Health Check

@app.get('/health')
def health():
    return {'status': 'ok'}

#Revenue API endpoint
@app.get('/api/revenue')
def revenue():
    df = load_csv("monthly_revenue.csv")
    return df.to_dict(orient='records')

# Top Customers API endpoint

@app.get('/api/top-customers')
def top_customers():
    df = load_csv("top_customers.csv")
    return df.to_dict(orient='records')

# Category API endpoint
@app.get('/api/categories')
def categories():
    df = load_csv('category_performance.csv')
    return df.to_dict(orient='records')

# Regional API endpoint

@app.get('/api/regions')
def regions():
    df = load_csv("regional_analysis.csv")
    return df.to_dict(orient='records')

