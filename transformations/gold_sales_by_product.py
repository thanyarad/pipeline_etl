from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum

# Initialize Spark session
spark = SparkSession.getActiveSession()
if spark is None:
    raise Exception("No active Spark session found")

# Define parameters
catalog = "main"
schema = "ecommerce"
silver_sales = f"{catalog}.{schema}.silver_sales"
silver_products = f"{catalog}.{schema}.silver_products"
gold_table = f"{catalog}.{schema}.gold_sales_by_product"

# Read silver tables
try:
    df_sales = spark.read.table(silver_sales)
    df_products = spark.read.table(silver_products)
except Exception as e:
    raise Exception(f"Failed to read silver tables: {e}")

# Aggregate sales by product
df_gold = (df_sales
    .join(df_products, "product_id", "inner")
    .groupBy("product_id", "product_name", "category")
    .agg(sum("quantity").alias("total_quantity"), sum(col("quantity") * col("price")).alias("total_revenue"))
)

# Write to gold Delta table
df_gold.write.format("delta").mode("overwrite").saveAsTable(gold_table)
print(f"Aggregated and saved {gold_table}")
