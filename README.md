# Pandas Receipts Analyzer

An end-to-end data analysis project using **Pandas** to clean, analyse, and visualise real-world retail transaction data.  
The project demonstrates reproducible data cleaning, aggregation, and reporting workflows on a large transactional dataset.

---

## 📊 Dataset

**Source:** Online Retail II dataset (UCI / Kaggle)

The dataset contains transactional data for a UK-based online retailer, including:
- invoice numbers  
- product descriptions  
- quantities  
- prices  
- invoice dates  
- customer country  

**Raw data location:**  
`data/raw/online_retail_II.csv`

---

## 🎯 Project Objectives

This project aims to:
- Clean and prepare messy, real-world retail transaction data  
- Handle cancelled transactions and invalid values  
- Engineer meaningful features for analysis  
- Analyse revenue trends over time  
- Identify top-performing countries and products  
- Produce reproducible outputs (CSV tables and plots)

---

## 🧹 Data Cleaning Steps

The following steps are applied to the raw dataset:

- Parse invoice dates into datetime format  
- Remove rows with missing critical values  
- Exclude cancelled invoices (InvoiceNo starting with `"C"`)  
- Remove transactions with non-positive quantities or prices  
- Create derived features:
  - `TotalPrice = Quantity × UnitPrice`
  - `YearMonth` for monthly aggregation  
- Standardise text fields (product descriptions and country names)

**Cleaned dataset saved to:**  
`data/processed/online_retail_clean.csv`

---

## 📈 Analysis Performed

The analysis includes:
- Monthly revenue trends  
- Top 10 countries by total revenue  
- Top 10 products by total revenue  

**Summary tables saved to:**  
`data/processed/`

**Generated visualisations saved to:**  
`reports/figures/`

---

## 📁 Project Structure

pandas-receipts-analyzer/
├── README.md
├── requirements.txt
├── data/
│ ├── raw/
│ │ └── online_retail_II.csv
│ └── processed/
├── src/
│ └── receipts_analysis.py
├── notebooks/
└── reports/
└── figures/


---

## ▶️ How to Run the Analysis

1. Install dependencies:
```bash
pip install -r requirements.txt
python src/receipts_analysis.py

