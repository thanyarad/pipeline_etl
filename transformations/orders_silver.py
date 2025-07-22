from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType

# Initialize Spark session
spark = SparkSession.getActiveSession()
if spark is None:
    raise Exception("No active Spark session found")

# Define schema
orders_schema = StructType([
    StructField("order_id", StringType(), False),
    StructField("customer_id", StringType(), False),
    StructField("order_date", TimestampType(), True),
    StructField("total_amount", DoubleType(), True)
])

# Define parameters
catalog = "main"
schema = "ecommerce"
bronze_table = f"{catalog}.{schema}.bronze_orders"
silver_table = f"{catalog}.{schema}.silver_orders"

# Read bronze table
df = spark.read.table(bronze_table)

# Clean and transform
df_transformed = (df
    .filter(col("order_id").isNotNull() & col("customer_id").isNotNull())
    .dropDuplicates(["order_id"])
    .withColumn("total_amount", when(col("total_amount") < 0, 0).otherwise(col("total_amount")))
)

# Write to silver Delta table
df_transformed.write.format("delta").mode("overwrite").saveAsTable(silver_table)
print(f"Transformed and saved {silver_table}")