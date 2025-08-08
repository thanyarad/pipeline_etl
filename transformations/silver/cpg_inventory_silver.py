from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType

df = spark.read.table("cpg_industry.bronze.cpg_inventory")

df_clean = (
    df.dropDuplicates(["inventory_id"])
      .dropna(subset=["inventory_id", "product_id", "stock_quantity"])
      .withColumn("stock_quantity", col("stock_quantity").cast(IntegerType()))
)

df_clean.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.silver.cpg_inventory")
