from pyspark.sql.functions import input_file_name, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType

# Define schema for cpg_distributor
cpg_distributor_schema = StructType([
    StructField("distributor_id", StringType()),
    StructField("distributor_name", StringType()),
    StructField("company_name", StringType()),
    StructField("last_activity_date", StringType()),
    StructField("no_of_associated_deals", IntegerType()),
    StructField("total_open_deal_value", StringType()),
    StructField("rating", StringType()),
    StructField("email", StringType()),
    StructField("phone", StringType()),
    StructField("city", StringType()),
    StructField("state", StringType()),
    StructField("country", StringType()),
    StructField("address", StringType()),
])


# Load JSON from volume
df_raw = (
    spark.read
    .schema(cpg_distributor_schema)
    .json("dbfs:/Volumes/cpg_industry/cpg_data/data/cpg_distributor/cpg_distributor.json")
)

# Write to Delta Table
df_raw.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.bronze.cpg_distributor")
