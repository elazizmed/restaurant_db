# 📊 Restaurant Sales Data Exporter

A Python script that retrieves restaurant sales data from a MySQL database and exports it to an Excel file for further analysis.

## 📌 Features
- Connects to a **MySQL database** (`restaurant_db`).
- Executes SQL queries to analyze **sales, income, charges, and passive income**.
- Saves results as **Excel spreadsheets** in the `excel_data` folder.
- Automatically **creates or updates** an Excel file (`orders_and_products.xlsx`).
- Summarizes **total income, charges, and passive income**.

## 🚀 Installation & Usage

### 1️⃣ Prerequisites
Ensure you have **Python 3.x** installed along with the required libraries:
```bash
pip install mysql-connector-python pandas xlsxwriter openpyxl