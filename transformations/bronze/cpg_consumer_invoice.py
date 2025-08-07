from pyspark.sql.functions import input_file_name, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType

# Define schema for cpg_consumer_invoice
cpg_consumer_invoice_schema = StructType([
    StructField("invoice_id", StringType()),
    StructField("order_id", StringType()),
    StructField("consumer_id", StringType()),
    StructField("invoice_date", StringType()),
    StructField("total_items", IntegerType()),
    StructField("gross_amount", StringType()),
    StructField("discount_amount", StringType()),
    StructField("tax_amount", StringType()),
    StructField("net_amount", StringType()),
    StructField("payment_method", StringType()),
    StructField("invoice_status", StringType()),
])


# Load JSON from volume
df_raw = (
    spark.read
    .schema(cpg_consumer_invoice_schema)
    .json("dbfs:/Volumes/cpg_industry/cpg_data/data/cpg_consumer/cpg_consumer_invoice.json")
    .withColumn("ingestion_time", current_timestamp())
)

# Write to Delta Table
df_raw.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.bronze.cpg_consumer_invoice")
