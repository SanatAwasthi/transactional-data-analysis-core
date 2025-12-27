import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" 

def load_data():
    """
    Load all core datasets required for transactional analysis.
    """
    orders = pd.read_csv(DATA_PATH / "olist_orders_dataset.csv")
    payments = pd.read_csv(DATA_PATH / "olist_order_payments_dataset.csv")
    items = pd.read_csv(DATA_PATH / "olist_order_items_dataset.csv")
    sellers = pd.read_csv(DATA_PATH / "olist_sellers_dataset.csv")

    return orders, payments, items, sellers

if __name__ == "__main__":
    orders, payments, items, sellers = load_data()
    print("Orders:", orders.shape)
    print("Payments:", payments.shape)
    print("Items:", items.shape)
    print("Sellers:", sellers.shape)