from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType, FloatType

df = spark.read.table("cpg_industry.bronze.cpg_distributor")

df_clean = (
    df.dropDuplicates(["distributor_id"])
      .dropna(subset=["distributor_id", "company_name"])
      .withColumn("no_of_associated_deals", col("no_of_associated_deals").cast(IntegerType()))
      .withColumn("total_open_deal_value", col("total_open_deal_value").cast(FloatType()))
      .withColumn("rating", col("rating").cast(FloatType()))
)

df_clean.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.silver.cpg_distributor")
