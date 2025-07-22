from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize Spark session
spark = SparkSession.getActiveSession()
if spark is None:
    raise Exception("No active Spark session found")

# Define parameters (replace TABLE_NAME)
catalog = "main"
schema = "ecommerce"
table_name = "TABLE_NAME"  # e.g., inventory
silver_table = f"{catalog}.{schema}.silver_{table_name}"
gold_table = f"{catalog}.{schema}.gold_{table_name}"

# Read silver table
try:
    df = spark.read.table(silver_table)
except Exception as e:
    raise Exception(f"Failed to read {silver_table}: {e}")

# Transform (customize as needed)
df_gold = df.groupBy("id").agg(count("id").alias("count"))

# Write to gold Delta table
df_gold.write.format("delta").mode("overwrite").saveAsTable(gold_table)
print(f"Aggregated and saved {gold_table}")