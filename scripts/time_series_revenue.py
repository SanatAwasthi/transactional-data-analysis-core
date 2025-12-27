import sys
from pathlib import Path

# Make project root visible
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from scripts.load_data import load_data
import pandas as pd

def build_daily_revenue(orders, payments):
    """
    Build daily revenue from order purchase date.
    """

    # Merge orders with payments
    df = orders.merge(payments, on="order_id", how="left")

    # Convert timestamp
    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"]
    )

    # Aggregate daily revenue
    daily_revenue = (
        df
        .groupby(df["order_purchase_timestamp"].dt.date)["payment_value"]
        .sum()
        .reset_index(name="daily_revenue")
    )

    return daily_revenue

def build_monthly_revenue(daily_revenue):
    """
    Aggregate daily revenue into monthly and calculate MoM growth.
    """

    daily_revenue["month"] = pd.to_datetime(
        daily_revenue["order_purchase_timestamp"]
    ).dt.to_period("M")

    monthly = (
        daily_revenue
        .groupby("month")["daily_revenue"]
        .sum()
        .reset_index()
    )

    monthly["mom_growth_pct"] = (
        monthly["daily_revenue"]
        .pct_change() * 100
    )

    return monthly

if __name__ == "__main__":
    orders, payments, _, _ = load_data()

    daily_revenue = build_daily_revenue(orders, payments)
    monthly_revenue = build_monthly_revenue(daily_revenue)

    print("Number of days:", daily_revenue.shape[0])
    print("\nTop revenue months:")
    print(monthly_revenue.sort_values("daily_revenue", ascending=False).head(3))

    print("\nHighest MoM growth:")
    print(monthly_revenue.sort_values("mom_growth_pct", ascending=False).head(3))
