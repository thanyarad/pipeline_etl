from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType, BooleanType

df = spark.read.table("cpg_industry.bronze.cpg_consumer")

df_clean = (
    df.dropDuplicates(["consumer_id"])
      .dropna(subset=["consumer_id", "email", "registration_date"])
      .withColumn("age", col("age").cast(IntegerType()))
      .withColumn("is_active", col("is_active").cast(BooleanType()))
)

df_clean.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.silver.cpg_consumer")
