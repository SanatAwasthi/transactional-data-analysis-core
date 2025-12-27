Transactional Data Analysis – Fintech Case Study

Project Overview:
This project analyzes real-world transactional data to evaluate revenue performance, data quality, and seller contribution patterns. The analysis mirrors real fintech use cases such as payment reconciliation, time-series revenue analysis, and revenue concentration risk assessment.

The dataset used contains over 100,000 transactions spanning 633 days, enabling robust trend and validation analysis.


Business Objectives:
1. Validate transactional and payment data integrity
2. Analyze daily and monthly revenue trends
3. Identify revenue growth and decline periods
4. Perform seller-level revenue contribution and concentration analysis
5. Highlight data quality risks and assumptions


Dataset:
Source: Brazilian E-Commerce Public Dataset (Olist)  
Key Tables Used:
1. orders
2. order_payments
3. order_items
4. sellers


Data Understanding & Validation:
1. Verified uniqueness of orders
2. Identified split-payment patterns across transactions
3. Reconciled orders and payments to ensure revenue accuracy
4. Detected a delivered order without a corresponding payment record (high-severity anomaly)

Key Finding:
1. ~2.7% of orders involve multiple payment records
2. 1 delivered order was missing a payment entry, indicating a potential reconciliation issue

Time-Series Revenue Analysis:
1. Built validated daily and monthly revenue datasets
2. Analyzed 633 days of revenue data
3. Identified:
  a. Best revenue month: Jan 2017
  b. Worst revenue month: Nov 2016
  c. Highest MoM growth: Apr 2018
  d. No zero-revenue days observed

Seller-Level Contribution Analysis
1. Analyzed revenue contribution across 3,095 sellers
2. Performed Pareto (80/20) analysis
3. ~18% of sellers contribute ~80% of total revenue

Insight: 
Revenue is highly concentrated, indicating dependency on a small subset of sellers.


Assumptions & Data Quality Risks
Assumptions:
1. 'payment_value' represents gross revenue
2. Payments are attributed to sellers at order level due to lack of item-level payment data
3. Delivered orders are expected to have payment records

Data Quality Risks Identified
1. Delivered order without payment (critical)
2. Presence of split payments requiring careful aggregation

Tools & Technologies
1. Python (Pandas, NumPy)
2. SQL (conceptual validation logic)
3. VS Code
4. GitHub

Key Takeaways
1. Demonstrated end-to-end transactional data analysis
2. Applied real-world data validation and reconciliation techniques
3. Translated raw transaction data into actionable business insights
4. Highlighted revenue concentration and operational risks
