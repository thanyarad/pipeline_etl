from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize Spark session
spark = SparkSession.getActiveSession()
if spark is None:
    raise Exception("No active Spark session found")

# Define table names and primary keys
catalog = "main"
schema = "ecommerce"
tables = {
    "bronze_products": ("main.ecommerce.bronze_products", "product_id"),
    "bronze_product_details": ("main.ecommerce.bronze_product_details", "id"),
    "bronze_product_families": ("main.ecommerce.bronze_product_families", "id"),
    "bronze_product_brands": ("main.ecommerce.bronze_product_brands", "id"),
    "bronze_product_classes": ("main.ecommerce.bronze_product_classes", "id"),
    "bronze_product_lines": ("main.ecommerce.bronze_product_lines", "id"),
    "bronze_product_types": ("main.ecommerce.bronze_product_types", "id"),
    "bronze_customers": ("main.ecommerce.bronze_customers", "customer_id"),
    "bronze_customer_address": ("main.ecommerce.bronze_customer_address", "id"),
    "bronze_customer_contact": ("main.ecommerce.bronze_customer_contact", "id"),
    "bronze_orders": ("main.ecommerce.bronze_orders", "order_id"),
    "bronze_sales": ("main.ecommerce.bronze_sales", "sale_id"),
    "bronze_sales_discount_tax": ("main.ecommerce.bronze_sales_discount_tax", "id"),
    "bronze_sales_fulfillment": ("main.ecommerce.bronze_sales_fulfillment", "id"),
    "bronze_sales_payment": ("main.ecommerce.bronze_sales_payment", "id"),
    "bronze_inventory": ("main.ecommerce.bronze_inventory", "id"),
    "bronze_suppliers": ("main.ecommerce.bronze_suppliers", "id"),
    "silver_products": ("main.ecommerce.silver_products", "product_id"),
    "silver_product_details": ("main.ecommerce.silver_product_details", "id"),
    "silver_customers": ("main.ecommerce.silver_customers", "customer_id"),
    "silver_orders": ("main.ecommerce.silver_orders", "order_id"),
    "silver_sales": ("main.ecommerce.silver_sales", "sale_id"),
    "gold_sales_by_product": ("main.ecommerce.gold_sales_by_product", "product_id"),
    "gold_customer_purchases": ("main.ecommerce.gold_customer_purchases", "customer_id")
}

# Validation function
def validate_table(table_name, primary_key):
    try:
        df = spark.table(table_name)
        null_count = df.filter(col(primary_key).isNull()).count()
        row_count = df.count()
        if null_count > 0:
            print(f"Validation failed for {table_name}: {null_count} null values in {primary_key}")
        else:
            print(f"Validation passed for {table_name}: {row_count} rows")
    except Exception as e:
        print(f"Validation failed for {table_name}: {e}")

# Validate all tables
for table_name, (full_table_name, pk) in tables.items():
    validate_table(full_table_name, pk)