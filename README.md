# 📊 Business Analytics Dashboard (FastAPI + Frontend)

A full-stack **business analytics dashboard** that transforms raw CSV data into meaningful business insights and visualizes them through an interactive web interface.

---

## 🚀 Overview
This project focuses on **data analytics + backend APIs + frontend visualization**:
- 📦 Raw data stored in CSV format  
- 🔄 Data cleaning & transformation using Python scripts  
- 📊 Business insights generation (revenue, customers, regions, categories)  
- 🌐 REST APIs using FastAPI  
- 📈 Interactive dashboard using Chart.js  

---

## ✨ Features
### 🔹 Data Processing
- Handles raw customer, order, and product data  
- Cleans missing and inconsistent values  
- Computes:
  - Monthly revenue trends  
  - Category-wise performance  
  - Regional analytics  
  - Top customers with churn flag  

### 🔹 Backend (FastAPI)
- Lightweight REST API  
- Serves processed analytics data  
- Modular CSV-based data loading  
- CORS enabled for frontend integration  

### 🔹 Frontend Dashboard
- Modern dark-themed UI  
- Revenue trend visualization 📈  
- Category performance charts 📊  
- Top customers table 🧑‍💼  
- Regional insights 🌍  
- Real-time API integration  

---

## ⚙️ Backend Setup (FastAPI)
### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
2️⃣ Run backend server
bash
cd backend
uvicorn main:app --reload
Backend runs at: http://127.0.0.1:8000

📡 API Endpoints
Endpoint	Description
/health	Health check
/api/revenue	Monthly revenue data
/api/categories	Category performance
/api/top-customers	Top customers
/api/regions	Regional analytics


🎨 Frontend Setup
Simply open: frontend/index.html  
OR run using Live Server (VS Code recommended).

🧪 Running Tests
bash
pytest -v
Tests included:

API response validation

Data loading checks from scripts

📊 Data Pipeline
Synthetic data is generated using:

Faker for names/emails

Randomized orders, products, and regions

Pipeline steps:

generate_data.py → Creates raw CSV files

clean_data.py → Cleans missing values, normalizes formats

analyze.py → Aggregates metrics, generates analytics datasets

📦 Requirements
fastapi

uvicorn

pandas

numpy

faker

pytest

httpx

🎨 Frontend Features
Dark modern dashboard UI

Chart.js visualizations

Responsive cards layout

Dynamic table rendering

Error handling for API failures

⚠️ Known Issues / Notes
Ensure backend is running before opening frontend

CSV files are generated dynamically in data/raw

If APIs fail, check backend logs and data folder

🚀 Future Improvements
Docker containerization

Real database integration (PostgreSQL)

Authentication system

Scheduled pipeline (cron/worker)

👨‍💻 Author
Aniket Paswan