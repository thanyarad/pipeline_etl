from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType, FloatType

df = spark.read.table("cpg_industry.bronze.cpg_consumer_order")

df_clean = (
    df.dropDuplicates(["order_id"])
      .dropna(subset=["order_id", "consumer_id", "product_id"])
      .withColumn("quantity", col("quantity").cast(IntegerType()))
      .withColumn("unit_price", col("unit_price").cast(FloatType()))
)

df_clean.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.silver.cpg_consumer_order")
