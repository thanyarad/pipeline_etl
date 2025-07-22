from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, concat_ws
from pyspark.sql.types import StructType, StructField, StringType

# Initialize Spark session
spark = SparkSession.getActiveSession()
if spark is None:
    raise Exception("No active Spark session found")

# Define schema
customers_schema = StructType([
    StructField("customer_id", StringType(), False),
    StructField("first_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("email", StringType(), True)
])

# Define parameters
catalog = "main"
schema = "ecommerce"
bronze_table = f"{catalog}.{schema}.bronze_customers"
silver_table = f"{catalog}.{schema}.silver_customers"

# Read bronze table
df = spark.read.table(bronze_table)

# Clean and transform
df_transformed = (df
    .filter(col("customer_id").isNotNull())
    .dropDuplicates(["customer_id"])
    .withColumn("first_name", trim(col("first_name")))
    .withColumn("last_name", trim(col("last_name")))
    .withColumn("full_name", concat_ws(" ", col("first_name"), col("last_name")))
)

# Write to silver Delta table
df_transformed.write.format("delta").mode("overwrite").saveAsTable(silver_table)
print(f"Transformed and saved {silver_table}")