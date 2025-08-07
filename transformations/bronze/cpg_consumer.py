from pyspark.sql.functions import col, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType

# Define schema for cpg_consumer
cpg_consumer_schema = StructType([
    StructField("consumer_id", StringType()),
    StructField("name", StringType()),
    StructField("email", StringType()),
    StructField("phone", StringType()),
    StructField("gender", StringType()),
    StructField("age", IntegerType()),
    StructField("registration_date", StringType()),
    StructField("is_active", BooleanType()),
    StructField("address", StringType()),
    StructField("city", StringType()),
    StructField("state", StringType()),
    StructField("country", StringType())
])

# Load JSON from volume using _metadata.file_path instead of input_file_name()
df_raw = (
    spark.read
    .schema(cpg_consumer_schema)
    .option("mergeSchema", "true")
    .json("dbfs:/Volumes/cpg_industry/cpg_data/data/cpg_consumer/cpg_consumer.json")
    .withColumn("source_file", col("_metadata.file_path"))
    .withColumn("ingestion_time", current_timestamp())
)

# Write to Delta Table in Bronze Layer
df_raw.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.bronze.cpg_consumer")
