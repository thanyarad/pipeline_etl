from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

# Initialize Spark session
spark = SparkSession.getActiveSession()
if spark is None:
    raise Exception("No active Spark session found")

# Define schemas
products_schema = StructType([
    StructField("product_id", StringType(), False),
    StructField("product_name", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("category", StringType(), True),
    StructField("stock", IntegerType(), True)
])
customers_schema = StructType([
    StructField("customer_id", StringType(), False),
    StructField("first_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("email", StringType(), True)
])
orders_schema = StructType([
    StructField("order_id", StringType(), False),
    StructField("customer_id", StringType(), False),
    StructField("order_date", TimestampType(), True),
    StructField("total_amount", DoubleType(), True)
])
sales_schema = StructType([
    StructField("sale_id", StringType(), False),
    StructField("order_id", StringType(), False),
    StructField("product_id", StringType(), False),
    StructField("quantity", IntegerType(), True),
    StructField("sale_date", TimestampType(), True)
])
generic_schema = StructType([
    StructField("id", StringType(), False),
    StructField("name", StringType(), True),
    StructField("value", StringType(), True)
])

# Define file paths and table names
catalog = "main"
schema = "ecommerce"
volume = "bronze"
file_paths = {
    "products": f"/Volumes/{catalog}/{schema}/{volume}/products.csv",
    "product_details": f"/Volumes/{catalog}/{schema}/{volume}/product_details.csv",
    "product_families": f"/Volumes/{catalog}/{schema}/{volume}/product_families.csv",
    "product_brands": f"/Volumes/{catalog}/{schema}/{volume}/product_brands.csv",
    "product_classes": f"/Volumes/{catalog}/{schema}/{volume}/product_classes.csv",
    "product_lines": f"/Volumes/{catalog}/{schema}/{volume}/product_lines.csv",
    "product_types": f"/Volumes/{catalog}/{schema}/{volume}/product_types.csv",
    "customers": f"/Volumes/{catalog}/{schema}/{volume}/customers.csv",
    "customer_address": f"/Volumes/{catalog}/{schema}/{volume}/customer_address.csv",
    "customer_contact": f"/Volumes/{catalog}/{schema}/{volume}/customer_contact.csv",
    "orders": f"/Volumes/{catalog}/{schema}/{volume}/orders.csv",
    "sales": f"/Volumes/{catalog}/{schema}/{volume}/sales.csv",
    "sales_discount_tax": f"/Volumes/{catalog}/{schema}/{volume}/sales_discount_tax.csv",
    "sales_fulfillment": f"/Volumes/{catalog}/{schema}/{volume}/sales_fulfillment.csv",
    "sales_payment": f"/Volumes/{catalog}/{schema}/{volume}/sales_payment.csv",
    "inventory": f"/Volumes/{catalog}/{schema}/{volume}/inventory.csv",
    "suppliers": f"/Volumes/{catalog}/{schema}/{volume}/suppliers.csv"
}
table_names = {
    "products": f"{catalog}.{schema}.bronze_products",
    "product_details": f"{catalog}.{schema}.bronze_product_details",
    "product_families": f"{catalog}.{schema}.bronze_product_families",
    "product_brands": f"{catalog}.{schema}.bronze_product_brands",
    "product_classes": f"{catalog}.{schema}.bronze_product_classes",
    "product_lines": f"{catalog}.{schema}.bronze_product_lines",
    "product_types": f"{catalog}.{schema}.bronze_product_types",
    "customers": f"{catalog}.{schema}.bronze_customers",
    "customer_address": f"{catalog}.{schema}.bronze_customer_address",
    "customer_contact": f"{catalog}.{schema}.bronze_customer_contact",
    "orders": f"{catalog}.{schema}.bronze_orders",
    "sales": f"{catalog}.{schema}.bronze_sales",
    "sales_discount_tax": f"{catalog}.{schema}.bronze_sales_discount_tax",
    "sales_fulfillment": f"{catalog}.{schema}.bronze_sales_fulfillment",
    "sales_payment": f"{catalog}.{schema}.bronze_sales_payment",
    "inventory": f"{catalog}.{schema}.bronze_inventory",
    "suppliers": f"{catalog}.{schema}.bronze_suppliers"
}
schemas = {
    "products": products_schema,
    "customers": customers_schema,
    "orders": orders_schema,
    "sales": sales_schema,
    "product_details": generic_schema,
    "product_families": generic_schema,
    "product_brands": generic_schema,
    "product_classes": generic_schema,
    "product_lines": generic_schema,
    "product_types": generic_schema,
    "customer_address": generic_schema,
    "customer_contact": generic_schema,
    "sales_discount_tax": generic_schema,
    "sales_fulfillment": generic_schema,
    "sales_payment": generic_schema,
    "inventory": generic_schema,
    "suppliers": generic_schema
}

# Ingest CSVs to bronze Delta tables
for table_name, file_path in file_paths.items():
    try:
        df = spark.read.option("header", "true").schema(schemas[table_name]).csv(file_path)
        delta_table = table_names[table_name]
        df.write.format("delta").mode("overwrite").saveAsTable(delta_table)
        print(f"Ingested {file_path} to {delta_table}")
    except Exception as e:
        print(f"Error ingesting {table_name}: {e}")