from pyspark.sql.functions import input_file_name, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType

# Define schema for cpg_consumer_order
cpg_consumer_order_schema = StructType([
    StructField("order_id", StringType()),
    StructField("consumer_id", StringType()),
    StructField("order_date", StringType()),
    StructField("shipping_address", StringType()),
    StructField("billing_address", StringType()),
    StructField("order_status", StringType()),
    StructField("total_amount", StringType()),
    StructField("payment_method", StringType()),
    StructField("currency", StringType()),
    StructField("channel", StringType()),
])


# Load JSON from volume
df_raw = (
    spark.read
    .schema(cpg_consumer_order_schema)
    .json("dbfs:/Volumes/cpg_industry/cpg_data/data/cpg_consumer/cpg_consumer_order.json")
    .withColumn("ingestion_time", current_timestamp())
)

# Write to Delta Table
df_raw.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.bronze.cpg_consumer_order")
