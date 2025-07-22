from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count

# Initialize Spark session
spark = SparkSession.getActiveSession()
if spark is None:
    raise Exception("No active Spark session found")

# Define parameters
catalog = "main"
schema = "ecommerce"
silver_orders = f"{catalog}.{schema}.silver_orders"
silver_customers = f"{catalog}.{schema}.silver_customers"
gold_table = f"{catalog}.{schema}.gold_customer_purchases"

# Read silver tables
try:
    df_orders = spark.read.table(silver_orders)
    df_customers = spark.read.table(silver_customers)
except Exception as e:
    raise Exception(f"Failed to read silver tables: {e}")

# Aggregate customer purchases
df_gold = (df_orders
    .join(df_customers, "customer_id", "inner")
    .groupBy("customer_id", "full_name")
    .agg(
        count("order_id").alias("total_orders"),
        sum("total_amount").alias("total_spent")
    )
)

# Write to gold Delta table
df_gold.write.format("delta").mode("overwrite").saveAsTable(gold_table)
print(f"Aggregated and saved {gold_table}")