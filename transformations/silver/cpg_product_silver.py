from pyspark.sql.functions import col

df = spark.read.table("cpg_industry.bronze.cpg_product")

df_clean = (
    df.dropDuplicates(["product_id"])
      .dropna(subset=["product_id", "product_name", "gtin", "sku_id"])
)

df_clean.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.silver.cpg_product")
