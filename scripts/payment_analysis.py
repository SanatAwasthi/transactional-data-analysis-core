import sys
from pathlib import Path

# Make project root visible to Python
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from scripts.load_data import load_data

def analyze_payment_distribution(payments):
    """
    Analyze how many payments each order has.
    """

    # Count number of payment records per order
    payment_counts = payments.groupby("order_id").size()

    # Distribution: how many orders have 1, 2, 3... payments
    distribution = (
        payment_counts
        .value_counts()
        .sort_index()
    )

    print("\nPayment count distribution (payments per order):")
    for num_payments, order_count in distribution.items():
        print(f"{num_payments} payment(s): {order_count} orders")

    # Percentage of orders with multiple payments
    multi_payment_pct = (payment_counts > 1).mean() * 100
    print(f"\nOrders with multiple payments: {multi_payment_pct:.2f}%")

    return distribution

if __name__ == "__main__":
    _, payments, _, _ = load_data()
    analyze_payment_distribution(payments)
