from pyspark.sql.functions import input_file_name, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType

# Define schema for cpg_order_items
cpg_consumer_order_items_schema = StructType([
    StructField("order_item_id", StringType()),
    StructField("order_id", StringType()),
    StructField("product_id", StringType()),
    StructField("quantity", IntegerType()),
    StructField("unit_price", StringType()),
    StructField("total_price", StringType()),
])


# Load JSON from volume
df_raw = (
    spark.read
    .schema(cpg_consumer_order_items_schema)
    .json("dbfs:/Volumes/cpg_industry/cpg_data/data/cpg_consumer/cpg_consumer_order_items.json")
)

# Write to Delta Table
df_raw.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.bronze.cpg_order_items")
