from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType

# Initialize Spark session
spark = SparkSession.getActiveSession()
if spark is None:
    raise Exception("No active Spark session found")

# Define schema
generic_schema = StructType([
    StructField("id", StringType(), False),
    StructField("name", StringType(), True),
    StructField("value", StringType(), True)
])

# Define parameters
catalog = "main"
schema = "ecommerce"
table_name = "sales_discount_tax"
bronze_table = f"{catalog}.{schema}.bronze_{table_name}"
silver_table = f"{catalog}.{schema}.silver_{table_name}"

# Read bronze table
try:
    df = spark.read.table(bronze_table)
except Exception as e:
    raise Exception(f"Failed to read {bronze_table}: {e}")

# Clean and transform
df_transformed = (df
    .filter(col("id").isNotNull())
    .dropDuplicates(["id"])
)

# Write to silver Delta table
df_transformed.write.format("delta").mode("overwrite").saveAsTable(silver_table)
print(f"Transformed and saved {silver_table}")