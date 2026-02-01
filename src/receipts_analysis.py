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


def load_data(path: Path) -> pd.DataFrame:
    """Load raw Online Retail II data."""
    if not path.exists():
        raise FileNotFoundError(f"Raw data not found at: {path}")
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean Online Retail II dataset and engineer useful features."""
    df = df.copy()

    # Parse dates
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    # Drop rows missing critical fields
    df = df.dropna(
        subset=[
            "InvoiceNo",
            "StockCode",
            "Description",
            "Quantity",
            "InvoiceDate",
            "UnitPrice",
            "Country",
        ]
    )

    # Remove cancelled invoices (InvoiceNo starting with 'C')
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

    # Remove non-positive quantities/prices
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

    # Feature engineering
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)

    # Tidy text fields
    df["Description"] = df["Description"].astype(str).str.strip()
    df["Country"] = df["Country"].astype(str).str.strip()

    return df


def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("YearMonth", as_index=False)["TotalPrice"]
        .sum()
        .sort_values("YearMonth")
        .rename(columns={"TotalPrice": "Revenue"})
    )


def top_countries(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return (
        df.groupby("Country", as_index=False)["TotalPrice"]
        .sum()
        .sort_values("TotalPrice", ascending=False)
        .head(n)
        .rename(columns={"TotalPrice": "Revenue"})
    )


def top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return (
        df.groupby("Description", as_index=False)["TotalPrice"]
        .sum()
        .sort_values("TotalPrice", ascending=False)
        .head(n)
        .rename(columns={"TotalPrice": "Revenue"})
    )


def save_tables(df_clean: pd.DataFrame,
                monthly: pd.DataFrame,
                countries: pd.DataFrame,
                products: pd.DataFrame) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df_clean.to_csv(PROCESSED_DIR / "online_retail_clean.csv", index=False)
    monthly.to_csv(PROCESSED_DIR / "monthly_revenue.csv", index=False)
    countries.to_csv(PROCESSED_DIR / "country_revenue_top10.csv", index=False)
    products.to_csv(PROCESSED_DIR / "top_products.csv", index=False)


def make_plots(monthly: pd.DataFrame, countries: pd.DataFrame) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # Monthly revenue trend
    plt.figure()
    plt.plot(monthly["YearMonth"], monthly["Revenue"])
    plt.xticks(rotation=45)
    plt.xlabel("Year-Month")
    plt.ylabel("Revenue")
    plt.title("Monthly Revenue Trend")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "monthly_revenue_trend.png")
    plt.close()

    # Top 10 countries (horizontal bar chart)
    plt.figure()
    plt.barh(countries["Country"], countries["Revenue"])
    plt.xlabel("Revenue")
    plt.title("Top 10 Countries by Revenue")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "top_countries_revenue.png")
    plt.close()


def main() -> None:
    # Load + clean
    df_raw = load_data(RAW_DATA)
    df_clean = clean_data(df_raw)

    # Analysis tables
    monthly = monthly_revenue(df_clean)
    countries = top_countries(df_clean, n=10)
    products = top_products(df_clean, n=10)

    # Save outputs
    save_tables(df_clean, monthly, countries, products)
    make_plots(monthly, countries)

    # Print summary (useful when running locally)
    print("✅ Analysis complete")
    print(f"Rows (raw):   {len(df_raw):,}")
    print(f"Rows (clean): {len(df_clean):,}")
    print("\nMonthly revenue (head):")
    print(monthly.head(5).to_string(index=False))
    print("\nTop countries:")
    print(countries.to_string(index=False))
    print("\nTop products:")
    print(products.to_string(index=False))


if __name__ == "__main__":
    main()

