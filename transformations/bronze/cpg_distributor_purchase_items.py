from pyspark.sql.functions import input_file_name, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType

# Define schema for cpg_distributor_purchase_items
cpg_distributor_purchase_items_schema = StructType([
    StructField("purchase_item_id", StringType()),
    StructField("purchase_id", StringType()),
    StructField("product_id", StringType()),
    StructField("upc", StringType()),
    StructField("quantity_ordered", IntegerType()),
    StructField("unit_cost", StringType()),
    StructField("total_price", StringType()),
])


# Load JSON from volume
df_raw = (
    spark.read
    .schema(cpg_distributor_purchase_items_schema)
    .json("dbfs:/Volumes/cpg_industry/cpg_data/data/cpg_distributor/cpg_distributor_purchase_items.json")
)

# Write to Delta Table
df_raw.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.bronze.cpg_distributor_purchase_items")
