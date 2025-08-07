from pyspark.sql.functions import input_file_name, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType

# Define schema for cpg_inventory
cpg_inventory_schema = StructType([
    StructField("inventory_id", StringType()),
    StructField("product_id", StringType()),
    StructField("quantity_on_hand", IntegerType()),
    StructField("reorder_level", IntegerType()),
    StructField("reorder_quantity", IntegerType()),
    StructField("last_restock_date", StringType()),
    StructField("safety_stock_level", IntegerType()),
    StructField("inventory_status", StringType()),
    StructField("last_updated", StringType()),
    StructField("location_code", StringType()),
    StructField("location_name", StringType()),
    StructField("location_type", StringType()),
    StructField("location_is_active", BooleanType()),
    StructField("address", StringType()),
    StructField("city", StringType()),
    StructField("state", StringType()),
    StructField("country", StringType()),
    StructField("email", StringType()),
    StructField("phone", StringType()),
])


# Load JSON from volume
df_raw = (
    spark.read
    .schema(cpg_inventory_schema)
    .json("dbfs:/Volumes/cpg_industry/cpg_data/data/cpg_inventory/cpg_inventory.json")
)

# Write to Delta Table
df_raw.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.bronze.cpg_inventory")
