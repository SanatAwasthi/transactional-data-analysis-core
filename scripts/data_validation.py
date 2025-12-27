import sys
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from scripts.load_data import load_data

def validate_orders_and_payments(orders, payments):
    print("Unique orders:", orders['order_id'].nunique())
    print("Orders with payments:", payments['order_id'].nunique())

    missing = set(orders['order_id']) - set(payments['order_id'])
    print("Orders without payments:", len(missing))

if __name__ == "__main__":
    orders, payments, _, _ = load_data()
    validate_orders_and_payments(orders, payments)