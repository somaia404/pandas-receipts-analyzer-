from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Paths
# -----------------------------
ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = ROOT / "data" / "raw" / "online_retail_II.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
FIGURES_DIR = ROOT / "reports" / "figures"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(RAW_DATA)

# -----------------------------
# Clean data
# -----------------------------
df = df.copy()

# Parse dates
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

# Remove rows with missing critical values
df = df.dropna(subset=[
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "Country"
])

# Remove cancelled invoices (InvoiceNo starting with 'C')
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

# Remove negative or zero quantities and prices
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

# Create total price
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

# Create year-month column
df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)

# -----------------------------
# Save cleaned data
# -----------------------------
clean_path = PROCESSED_DIR / "online_retail_clean.csv"
df.to_csv(clean_path, index=False)

# -----------------------------
# Analysis
# -----------------------------

# Monthly revenue
monthly_revenue = (
    df.groupby("YearMonth", as_index=False)["TotalPrice"]
    .sum()
    .sort_values("YearMonth")
)

# Revenue by country (top 10)
country_revenue = (
    df.groupby("Country", as_index=False)["TotalPrice"]
    .sum()
    .sort_values("TotalPrice", ascending=False)
    .head(10)
)

# Top products by revenue
top_products = (
    df.groupby("Description", as_index=False)["TotalPrice"]
    .sum()
    .sort_values("TotalPrice", ascending=False)
    .head(10)
)

# -----------------------------
# Save analysis outputs
# -----------------------------
monthly_revenue.to_csv(PROCESSED_DIR / "monthly_revenue.csv", index=False)
country_revenue.to_csv(PROCESSED_DIR / "country_revenue_top10.csv", index=False)
top_products.to_csv(PROCESSED_DIR / "top_products.csv", index=False)

# -----------------------------
# Visualisations
# -----------------------------

# Monthly revenue trend
plt.figure()
plt.plot(monthly_revenue["YearMonth"], monthly_revenue["TotalPrice"])
plt.xticks(rotation=45)
plt.xlabel("Year-Month")
plt.ylabel("Revenue")
plt.title("Monthly Revenue Trend")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "monthly_revenue_trend.png")
plt.close()

# Top countries
plt.figure()
plt.barh(
    country_revenue["Country"],
    country_revenue["TotalPrice"]
)
plt.xlabel("Revenue")
plt.title("Top 10 Countries by Revenue")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(FIGURES_DIR / "top_countries_revenue.png")
plt.close()

print("Analysis complete.")
print(f"Clean data saved to: {clean_path}")
