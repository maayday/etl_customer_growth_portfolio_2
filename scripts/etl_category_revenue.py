# Step 1: Extract data from the database boilerplate code

import pandas as pd
import psycopg2
import logging
from datetime import datetime
from db import get_connection  # This imports your reusable DB connection

# Generate a timestamp for filenames/logs
today = datetime.now().strftime("%Y-%m-%d")

# Setup logging
log_path = f"../logs/category_revenue_{today}.log"
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("🚀 ETL Job Started: Monthly Revenue by Product Category")

# Connect to DB
conn = get_connection()
cur = conn.cursor()

#  STEP 3: Add the SQL Query (Extract + Transform)
query = """
SELECT 
    TO_CHAR(o.order_date, 'YYYY-MM') AS order_month,
    c.category_name,
    SUM(od.quantity * od.unit_price) AS total_revenue
FROM orders o
JOIN order_details od ON o.order_id = od.order_id
JOIN products p ON od.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY order_month, c.category_name
ORDER BY order_month, total_revenue DESC;
"""

cur.execute(query)
rows = cur.fetchall()
logging.info("📊 Query executed and data fetched.")

# Joins all necessary tables
# Groups by month and category
# Calculates total revenue
# Pulls your data into rows

# Step 4: Convert to DataFrame and Export to CSV

# Convert results to DataFrame
df = pd.DataFrame(rows, columns=["order_month", "category_name", "total_revenue"])

# Export to timestamped CSV
csv_path = f"../data/category_revenue_{today}.csv"
df.to_csv(csv_path, index=False)
logging.info(f"📦 Data exported to {csv_path}")

# A clean DataFrame
# A .csv file saved to your data/ folder with today’s date
# A log entry to confirm the save

# Step 5: Close Database Connection and Finalize the script

cur.close()
conn.close()
logging.info("✅ ETL Job Complete and Connection Closed")

print("✅ Monthly Category Revenue ETL completed successfully.")
