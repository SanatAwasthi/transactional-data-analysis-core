import pandas as pd
orders = pd.read_csv(r"C:\Users\sanat.awasthi\OneDrive - Pine Labs Private Limited\Documents\Projects\Transactional Data Analysis Project (CORE)\Data\Raw\olist_orders_dataset.csv")
payments = pd.read_csv(r"C:\Users\sanat.awasthi\OneDrive - Pine Labs Private Limited\Documents\Projects\Transactional Data Analysis Project (CORE)\Data\Raw\olist_order_payments_dataset.csv")

print("Orders")
print(orders.head())
print(orders.columns)
print("Rows: ",len(orders))

print("Payments")
print(payments.head())
print(payments.columns)
print("Rows: ",len(payments))

# orders have 99441 rows
# payments have 103886 rows
# There are more payment records than orders, indicating multiple payments per order
# Are all the entries unique in both datasets?

print("Unique Orders: ", orders['order_id'].nunique())
print("Unique Payments: ", payments['order_id'].nunique())

# Orders have 99441 unique order IDs, matching the total rows, so all orders are unique.
# Payments have 99440 unique order IDs but 103886 rows, confirming multiple payment entries. Also, one order ID is missing in payments.

missing_order = set(orders['order_id']) - set(payments['order_id'])
print("Missing Order ID in Payments: ", missing_order)
missed_order_df = orders[orders["order_id"].isin(missing_order)]
print(missed_order_df[['order_status','order_purchase_timestamp','order_approved_at', 'order_delivered_carrier_date',
       'order_delivered_customer_date', 'order_estimated_delivery_date']])
# Missing order is 'delivered', so it should have payment records. Why is it missing?

#How many orders have 1 payment, how many have 2?
#print(payments.groupby('order_id').size().value_counts().head())

#calculate total revenue
total_revenue = payments['payment_value'].sum()
#print("Total Revenue:", total_revenue)

orders_payments = orders.merge(
    payments,
    on='order_id',
    how='inner'
)
#print(orders_payments.columns)

orders_payments['order_purchase_timestamp'] = pd.to_datetime(
    orders_payments['order_purchase_timestamp']
)
#print(orders_payments['order_purchase_timestamp'])
orders_payments['order_date'] = orders_payments['order_purchase_timestamp'].dt.date
#print(orders_payments['order_date'])

#calculate daily revenue day-wise

daily_revenue = (
    orders_payments
    .groupby('order_date')['payment_value']
    .sum()
    .reset_index()
    .sort_values('order_date')
)
#print(daily_revenue)
#print("Daily revenue sum:", daily_revenue['payment_value'].sum())
#print("Total revenue:", total_revenue)

zero_revenue_days = daily_revenue[daily_revenue['payment_value'] == 0]

#print("Zero revenue days:", zero_revenue_days.shape[0])
#print(zero_revenue_days.head())

#Monthly Revenue
daily_revenue['order_date'] = pd.to_datetime(daily_revenue['order_date'])

monthly_revenue = (
    daily_revenue
    .set_index('order_date')
    .resample('M')['payment_value']
    .sum()
    .reset_index()
)

#print(monthly_revenue.head())
#print("Monthly sum:", monthly_revenue['payment_value'].sum())
#print("Total revenue:", total_revenue)

# Month-over-Month Growth
monthly_revenue['mom_growth'] = (
    monthly_revenue['payment_value']
    .pct_change() * 100
)
#print(monthly_revenue)

order_items = pd.read_csv(r"C:\Users\sanat.awasthi\OneDrive - Pine Labs Private Limited\Documents\Projects\Transactional Data Analysis Project (CORE)\Data\Raw\olist_order_items_dataset.csv")
sellers = pd.read_csv(r"C:\Users\sanat.awasthi\OneDrive - Pine Labs Private Limited\Documents\Projects\Transactional Data Analysis Project (CORE)\Data\Raw\olist_sellers_dataset.csv")

print(order_items.columns)
#Total number of sellers
print(len(sellers))
# Merge payments with order_items
payments_items = payments.merge(
    order_items,
    on='order_id',
    how='inner'
)

# Revenue per seller
seller_revenue = (
    payments_items
    .groupby('seller_id')['payment_value']
    .sum()
    .reset_index()
    .sort_values('payment_value', ascending=False)
)
#print(seller_revenue)

seller_revenue['cumulative_revenue'] = seller_revenue['payment_value'].cumsum()
total_revenue = seller_revenue['payment_value'].sum()
seller_revenue['cumulative_pct'] = (
    seller_revenue['cumulative_revenue'] / total_revenue * 100
)
#Number of sellers contributing to ~80% revenue
top_sellers_80 = seller_revenue[seller_revenue['cumulative_pct'] <= 80]

print("Number of sellers contributing to 80% revenue:", top_sellers_80.shape[0])
print("Total sellers:", seller_revenue.shape[0])

#Rough % of sellers driving most revenue

total_sellers = seller_revenue.shape[0]
top_sellers = top_sellers_80.shape[0]

pct_sellers_80 = (top_sellers / total_sellers) * 100

print(f"Percentage of sellers driving ~80% revenue: {pct_sellers_80:.2f}%")
