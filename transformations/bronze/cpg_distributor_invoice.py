from pyspark.sql.functions import input_file_name, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType

# Define schema for cpg_distributor_invoice
cpg_distributor_invoice_schema = StructType([
    StructField("invoice_id", StringType()),
    StructField("purchase_id", StringType()),
    StructField("invoice_date", StringType()),
    StructField("amount_due", StringType()),
    StructField("tax_amount", StringType()),
    StructField("discount", StringType()),
    StructField("total_payable", StringType()),
    StructField("payment_status", StringType()),
])


# Load JSON from volume
df_raw = (
    spark.read
    .schema(cpg_distributor_invoice_schema)
    .json("dbfs:/Volumes/cpg_industry/cpg_data/data/cpg_distributor/cpg_distributor_invoice.json")
)

# Write to Delta Table
df_raw.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.bronze.cpg_distributor_invoice")
