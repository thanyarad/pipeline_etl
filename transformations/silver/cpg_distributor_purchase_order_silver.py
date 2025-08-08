from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType, FloatType

df = spark.read.table("cpg_industry.bronze.cpg_distributor_purchase_order")

df_clean = (
    df.dropDuplicates(["purchase_order_id"])
      .dropna(subset=["purchase_order_id", "product_id", "quantity", "unit_cost"])
      .withColumn("quantity", col("quantity").cast(IntegerType()))
      .withColumn("unit_cost", col("unit_cost").cast(FloatType()))
)

df_clean.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.silver.cpg_distributor_purchase_order")
