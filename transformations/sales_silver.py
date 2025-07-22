from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType

# Initialize Spark session
spark = SparkSession.getActiveSession()
if spark is None:
    raise Exception("No active Spark session found")

# Define schema
sales_schema = StructType([
    StructField("sale_id", StringType(), False),
    StructField("order_id", StringType(), False),
    StructField("product_id", StringType(), False),
    StructField("quantity", IntegerType(), True),
    StructField("sale_date", TimestampType(), True)
])

# Define parameters
catalog = "main"
schema = "ecommerce"
bronze_table = f"{catalog}.{schema}.bronze_sales"
silver_table = f"{catalog}.{schema}.silver_sales"

# Read bronze table
df = spark.read.table(bronze_table)

# Clean and transform
df_transformed = (df
    .filter(col("sale_id").isNotNull() & col("order_id").isNotNull() & col("product_id").isNotNull())
    .dropDuplicates(["sale_id"])
    .withColumn("quantity", when(col("quantity") < 0, 0).otherwise(col("quantity")))
)

# Write to silver Delta table
df_transformed.write.format("delta").mode("overwrite").saveAsTable(silver_table)
print(f"Transformed and saved {silver_table}")