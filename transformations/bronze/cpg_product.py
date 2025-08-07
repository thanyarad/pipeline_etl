from pyspark.sql.functions import input_file_name, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType

# Define schema for cpg_product
cpg_product_schema = StructType([
    StructField("product_id", StringType()),
    StructField("sku_id", StringType()),
    StructField("upc", StringType()),
    StructField("gtin", StringType()),
    StructField("product_name", StringType()),
    StructField("description", StringType()),
    StructField("department", StringType()),
    StructField("category", StringType()),
    StructField("brand", StringType()),
    StructField("unit_of_measurement", StringType()),
    StructField("retail_price", StringType()),
    StructField("unit_price", StringType()),
    StructField("release_date", StringType()),
    StructField("expiration_days", IntegerType()),
    StructField("product_status", StringType()),
])


# Load JSON from volume
df_raw = (
    spark.read
    .schema(cpg_product_schema)
    .json("dbfs:/Volumes/cpg_industry/cpg_data/data/cpg_inventory/cpg_product.json")
)

# Write to Delta Table
df_raw.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.bronze.cpg_product")
