from pyspark.sql.functions import input_file_name, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType

# Define schema for cpg_distributor_purchases
cpg_distributor_purchases_schema = StructType([
    StructField("purchase_id", StringType()),
    StructField("order_date", StringType()),
    StructField("expected_delivery_date", StringType()),
    StructField("order_status", StringType()),
    StructField("total_amount", StringType()),
    StructField("currency", StringType()),
])


# Load JSON from volume
df_raw = (
    spark.read
    .schema(cpg_distributor_purchases_schema)
    .json("dbfs:/Volumes/cpg_industry/cpg_data/data/cpg_distributor/cpg_distributor_purchases.json")
)

# Write to Delta Table
df_raw.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.bronze.cpg_distributor_purchases")
