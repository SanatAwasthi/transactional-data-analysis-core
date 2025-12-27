import sys
from pathlib import Path

# Make project root visible
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from scripts.load_data import load_data
import pandas as pd

def build_seller_revenue(items, payments):
    """
    Allocate order-level revenue to sellers
    and compute cumulative contribution.
    """

    # Total revenue per order
    order_revenue = (
        payments
        .groupby("order_id")["payment_value"]
        .sum()
        .reset_index()
    )

    # Join with items to map sellers
    item_revenue = items.merge(order_revenue, on="order_id", how="inner")

    # Revenue per seller
    seller_revenue = (
        item_revenue
        .groupby("seller_id")["payment_value"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    # Cumulative percentage
    seller_revenue["cumulative_pct"] = (
        seller_revenue["payment_value"].cumsum()
        / seller_revenue["payment_value"].sum()
    )

    return seller_revenue

if __name__ == "__main__":
    _, payments, items, _ = load_data()

    seller_revenue = build_seller_revenue(items, payments)

    total_sellers = seller_revenue.shape[0]
    top_sellers = seller_revenue[seller_revenue["cumulative_pct"] <= 0.80]

    print("Total sellers:", total_sellers)
    print("Sellers contributing ~80% revenue:", top_sellers.shape[0])
    print(
        "Percentage of sellers driving most revenue:",
        round(top_sellers.shape[0] / total_sellers * 100, 2),
        "%"
    )
