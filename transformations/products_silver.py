from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, when
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

# Initialize Spark session
spark = SparkSession.getActiveSession()
if spark is None:
    raise Exception("No active Spark session found")

# Define schema
products_schema = StructType([
    StructField("product_id", StringType(), False),
    StructField("product_name", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("category", StringType(), True),
    StructField("stock", IntegerType(), True)
])

# Define parameters
catalog = "main"
schema = "ecommerce"
bronze_table = f"{catalog}.{schema}.bronze_products"
silver_table = f"{catalog}.{schema}.silver_products"

# Read bronze table
df = spark.read.table(bronze_table)

# Clean and transform
df_transformed = (df
    .filter(col("product_id").isNotNull())
    .dropDuplicates(["product_id"])
    .withColumn("product_name", trim(col("product_name")))
    .withColumn("price", when(col("price") < 0, 0).otherwise(col("price")))
)

# Write to silver Delta table
df_transformed.write.format("delta").mode("overwrite").saveAsTable(silver_table)
print(f"Transformed and saved {silver_table}")