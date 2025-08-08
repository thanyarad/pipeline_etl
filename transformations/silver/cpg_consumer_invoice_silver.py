from pyspark.sql.functions import col
from pyspark.sql.types import FloatType

df = spark.read.table("cpg_industry.bronze.cpg_consumer_invoice")

df_clean = (
    df.dropDuplicates(["invoice_id"])
      .dropna(subset=["invoice_id", "order_id", "invoice_date"])
      .withColumn("net_amount", col("net_amount").cast(FloatType()))
)

df_clean.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.silver.cpg_consumer_invoice")
