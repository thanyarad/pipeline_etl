# Silver Layer Transformation Script for cpg_consumer
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

# Silver Layer Transformation Script for cpg_consumer_order
df = spark.read.table("cpg_industry.bronze.cpg_consumer_order")
df_clean = (
    df.dropDuplicates(["order_id"])
      .dropna(subset=["order_id", "consumer_id", "order_date"])
)
df_clean.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.silver.cpg_consumer_order")

# Silver Layer Transformation Script for cpg_order_items
df = spark.read.table("cpg_industry.bronze.cpg_order_items")
df_clean = (
    df.dropDuplicates(["order_item_id"])
      .dropna(subset=["order_item_id", "order_id", "product_id"])
)
df_clean.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.silver.cpg_order_items")

# Silver Layer Transformation Script for cpg_consumer_invoice
df = spark.read.table("cpg_industry.bronze.cpg_consumer_invoice")
df_clean = (
    df.dropDuplicates(["invoice_id"])
      .dropna(subset=["invoice_id", "order_id", "consumer_id"])
)
df_clean.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.silver.cpg_consumer_invoice")

# Silver Layer Transformation Script for cpg_inventory
from pyspark.sql.types import StringType

df = spark.read.table("cpg_industry.bronze.cpg_inventory")
df_clean = (
    df.dropDuplicates(["inventory_id"])
      .dropna(subset=["inventory_id", "product_id"])
      .withColumn("location_type", col("location_type").cast(StringType()))
      .withColumn("location_is_active", col("location_is_active").cast(BooleanType()))
)
df_clean.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.silver.cpg_inventory")

# Silver Layer Transformation Script for cpg_product
df = spark.read.table("cpg_industry.bronze.cpg_product")
df_clean = (
    df.dropDuplicates(["product_id"])
      .dropna(subset=["product_id", "product_name"])
)
df_clean.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.silver.cpg_product")

# Silver Layer Transformation Script for cpg_distributor_purchases
df = spark.read.table("cpg_industry.bronze.cpg_distributor_purchases")
df_clean = (
    df.dropDuplicates(["purchase_id"])
      .dropna(subset=["purchase_id", "order_date"])
)
df_clean.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.silver.cpg_distributor_purchases")

# Silver Layer Transformation Script for cpg_distributor_purchase_items
df = spark.read.table("cpg_industry.bronze.cpg_distributor_purchase_items")
df_clean = (
    df.dropDuplicates(["purchase_item_id"])
      .dropna(subset=["purchase_item_id", "purchase_id", "product_id"])
)
df_clean.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.silver.cpg_distributor_purchase_items")

# Silver Layer Transformation Script for cpg_distributor_invoice
df = spark.read.table("cpg_industry.bronze.cpg_distributor_invoice")
df_clean = (
    df.dropDuplicates(["invoice_id"])
      .dropna(subset=["invoice_id", "purchase_id"])
)
df_clean.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.silver.cpg_distributor_invoice")

# Silver Layer Transformation Script for cpg_distributor
df = spark.read.table("cpg_industry.bronze.cpg_distributor")
df_clean = (
    df.dropDuplicates(["distributor_id"])
      .dropna(subset=["distributor_id", "distributor_name"])
)
df_clean.write.format("delta").mode("overwrite").saveAsTable("cpg_industry.silver.cpg_distributor")
