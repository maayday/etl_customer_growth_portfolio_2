
import psycopg2
import pandas as pd

# Step 1: Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="northwind",
    user="etl",
    password="demopass",
    host="localhost",
    port="5433"
)
cur = conn.cursor()
print("✅ Connected to PostgreSQL")

# Step 2: Query from the view
cur.execute("SELECT * FROM customer_growth_view")
rows = cur.fetchall()

# Step 3: Convert to DataFrame
df = pd.DataFrame(rows, columns=["join_month", "new_customers"])
print("📊 Data loaded into DataFrame")
print(df.head())

# Step 4: Save to CSV
df.to_csv("monthly_customer_growth.csv", index=False)
print("💾 Exported to monthly_customer_growth.csv")

# Step 5: Create summary table if needed
cur.execute("""
CREATE TABLE IF NOT EXISTS monthly_customer_growth (
    join_month VARCHAR(7),
    new_customers INT
);
""")
conn.commit()

# Step 6: Insert into table
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO monthly_customer_growth (join_month, new_customers)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING;
    """, (row["join_month"], row["new_customers"]))
conn.commit()
print("📥 Data inserted into monthly_customer_growth table")

# Step 7: Close connection
cur.close()
conn.close()
print("✅ ETL job complete!")

