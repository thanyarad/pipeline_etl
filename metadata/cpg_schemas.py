from pyspark.sql.types import *

# Manufacturer Profile
cpg_manufacturer_schema = StructType([
    StructField("manufacturer_id", IntegerType(), True),
    StructField("manufacturer_name", StringType(), True),
    StructField("legal_name", StringType(), True),
    StructField("company_code", StringType(), True),
    StructField("tax_id", StringType(), True),
    StructField("address", StringType(), True),
    StructField("email", StringType(), True),
    StructField("phone", StringType(), True),
    StructField("website", StringType(), True),
    StructField("location_id", IntegerType(), True),
    StructField("is_active", BooleanType(), True),
    StructField("created_at", TimestampType(), True),
    StructField("last_updated", TimestampType(), True)
])

# CPG Consumer
cpg_consumer_schema = StructType([
    StructField("consumer_id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("phone", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("registration_date", DateType(), True),
    StructField("is_active", BooleanType(), True),
    StructField("address", StringType(), True),
    StructField("location_id", IntegerType(), True)
])

# CPG Product
cpg_product_schema = StructType([
    StructField("product_id", IntegerType(), True),
    StructField("manufacturer_id", IntegerType(), True),
    StructField("sku_id", StringType(), True),
    StructField("upc", StringType(), True),
    StructField("gtin", StringType(), True),
    StructField("product_name", StringType(), True),
    StructField("description", StringType(), True),
    StructField("department", StringType(), True),
    StructField("category", StringType(), True),
    StructField("brand", StringType(), True),
    StructField("unit_of_measurement", StringType(), True),
    StructField("retail_price", FloatType(), True),
    StructField("release_date", DateType(), True),
    StructField("expiration_days", IntegerType(), True),
    StructField("product_status", StringType(), True)
])

# Consumer Order
cpg_consumer_order_schema = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("consumer_id", IntegerType(), True),
    StructField("order_date", DateType(), True),
    StructField("shipping_address", StringType(), True),
    StructField("billing_address", StringType(), True),
    StructField("order_status", StringType(), True),
    StructField("total_amount", FloatType(), True),
    StructField("payment_method", StringType(), True),
    StructField("currency", StringType(), True),
    StructField("channel", StringType(), True)
])

# Order Items
cpg_order_items_schema = StructType([
    StructField("order_item_id", IntegerType(), True),
    StructField("order_id", IntegerType(), True),
    StructField("product_id", IntegerType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("unit_price", FloatType(), True),
    StructField("total_price", FloatType(), True)
])

# Consumer Invoice
cpg_consumer_invoice_schema = StructType([
    StructField("invoice_id", IntegerType(), True),
    StructField("order_id", IntegerType(), True),
    StructField("consumer_id", IntegerType(), True),
    StructField("invoice_date", DateType(), True),
    StructField("total_items", IntegerType(), True),
    StructField("gross_amount", FloatType(), True),
    StructField("discount_amount", FloatType(), True),
    StructField("tax_amount", FloatType(), True),
    StructField("net_amount", FloatType(), True),
    StructField("payment_method", StringType(), True),
    StructField("invoice_status", StringType(), True)
])

# Product Inventory
cpg_product_inventory_schema = StructType([
    StructField("inventory_id", IntegerType(), True),
    StructField("product_id", IntegerType(), True),
    StructField("inventory_source_id", IntegerType(), True),
    StructField("quantity_on_hand", IntegerType(), True),
    StructField("reorder_level", IntegerType(), True),
    StructField("reorder_quantity", IntegerType(), True),
    StructField("last_restock_date", DateType(), True),
    StructField("safety_stock_level", IntegerType(), True),
    StructField("inventory_status", StringType(), True),
    StructField("last_updated", TimestampType(), True)
])

# Inventory Source
cpg_inventory_source_schema = StructType([
    StructField("inventory_source_id", IntegerType(), True),
    StructField("manufacturer_id", IntegerType(), True),
    StructField("source_code", StringType(), True),
    StructField("source_name", StringType(), True),
    StructField("source_type", StringType(), True),
    StructField("is_active", BooleanType(), True),
    StructField("location_id", IntegerType(), True),
    StructField("address", StringType(), True),
    StructField("email", StringType(), True),
    StructField("phone", StringType(), True)
])

# Manufacturer-Supplier Contract
cpg_supplier_contract_schema = StructType([
    StructField("contract_id", IntegerType(), True),
    StructField("manufacturer_id", IntegerType(), True),
    StructField("manufacturer_product_id", IntegerType(), True),
    StructField("supplier_id", IntegerType(), True),
    StructField("upc", StringType(), True),
    StructField("start_date", DateType(), True),
    StructField("end_date", DateType(), True),
    StructField("unit_price", FloatType(), True),
    StructField("currency", StringType(), True),
    StructField("contract_status", StringType(), True)
])

# Location
location_schema = StructType([
    StructField("location_id", IntegerType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("country", StringType(), True)
])
