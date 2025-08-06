from pyspark.sql.types import *

# Define all schemas based on the given metadata

schemas = {
    "cpg_consumer": StructType([
        StructField("consumer_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("email", StringType(), True),
        StructField("phone", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("age", IntegerType(), True),
        StructField("registration_date", DateType(), True),
        StructField("is_active", BooleanType(), True),
        StructField("address", StringType(), True),
        StructField("city", StringType(), True),
        StructField("state", StringType(), True),
        StructField("country", StringType(), True),
    ]),
    
    "cpg_product": StructType([
        StructField("product_id", IntegerType(), True),
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
        StructField("unit_price", FloatType(), True),
        StructField("release_date", DateType(), True),
        StructField("expiration_days", IntegerType(), True),
        StructField("product_status", StringType(), True),
    ]),

    "cpg_consumer_order": StructType([
        StructField("order_id", IntegerType(), True),
        StructField("consumer_id", IntegerType(), True),
        StructField("order_date", DateType(), True),
        StructField("shipping_address", StringType(), True),
        StructField("billing_address", StringType(), True),
        StructField("order_status", StringType(), True),
        StructField("total_amount", FloatType(), True),
        StructField("payment_method", StringType(), True),
        StructField("currency", StringType(), True),
        StructField("channel", StringType(), True),
    ]),

    "cpg_order_items": StructType([
        StructField("order_item_id", IntegerType(), True),
        StructField("order_id", IntegerType(), True),
        StructField("product_id", IntegerType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("unit_price", FloatType(), True),
        StructField("total_price", FloatType(), True),
    ]),

    "cpg_consumer_invoice": StructType([
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
        StructField("invoice_status", StringType(), True),
    ]),

    "cpg_inventory": StructType([
        StructField("inventory_id", IntegerType(), True),
        StructField("product_id", IntegerType(), True),
        StructField("quantity_on_hand", IntegerType(), True),
        StructField("reorder_level", IntegerType(), True),
        StructField("reorder_quantity", IntegerType(), True),
        StructField("last_restock_date", DateType(), True),
        StructField("safety_stock_level", IntegerType(), True),
        StructField("inventory_status", StringType(), True),
        StructField("last_updated", TimestampType(), True),
        StructField("location_code", StringType(), True),
        StructField("location_name", StringType(), True),
        StructField("location_type", StringType(), True),
        StructField("location_is_active", BooleanType(), True),
        StructField("address", StringType(), True),
        StructField("city", StringType(), True),
        StructField("state", StringType(), True),
        StructField("country", StringType(), True),
        StructField("email", StringType(), True),
        StructField("phone", StringType(), True),
    ]),

    "cpg_distributor_purchases": StructType([
        StructField("purchase_id", IntegerType(), True),
        StructField("order_date", DateType(), True),
        StructField("expected_delivery_date", DateType(), True),
        StructField("order_status", StringType(), True),
        StructField("total_amount", FloatType(), True),
        StructField("currency", StringType(), True),
    ]),

    "cpg_distributor_purchase_items": StructType([
        StructField("purchase_item_id", IntegerType(), True),
        StructField("purchase_id", IntegerType(), True),
        StructField("product_id", IntegerType(), True),
        StructField("upc", StringType(), True),
        StructField("quantity_ordered", IntegerType(), True),
        StructField("unit_cost", FloatType(), True),
        StructField("total_price", FloatType(), True),
    ]),

    "cpg_distributor_invoice": StructType([
        StructField("invoice_id", IntegerType(), True),
        StructField("purchase_id", IntegerType(), True),
        StructField("invoice_date", DateType(), True),
        StructField("amount_due", FloatType(), True),
        StructField("tax_amount", FloatType(), True),
        StructField("discount", FloatType(), True),
        StructField("total_payable", FloatType(), True),
        StructField("payment_status", StringType(), True),
    ]),

    "distributor_inventory": StructType([
        StructField("inventory_id", IntegerType(), True),
        StructField("distributor_id", IntegerType(), True),
        StructField("product_id", IntegerType(), True),
        StructField("quantity_on_hand", IntegerType(), True),
        StructField("reorder_level", IntegerType(), True),
        StructField("reorder_quantity", IntegerType(), True),
        StructField("last_restock_date", DateType(), True),
        StructField("safety_stock_level", IntegerType(), True),
        StructField("inventory_status", StringType(), True),
        StructField("last_updated", TimestampType(), True),
        StructField("location_code", StringType(), True),
        StructField("location_name", StringType(), True),
        StructField("location_type", StringType(), True),
        StructField("location_is_active", BooleanType(), True),
        StructField("address", StringType(), True),
        StructField("city", StringType(), True),
        StructField("state", StringType(), True),
        StructField("country", StringType(), True),
        StructField("email", StringType(), True),
        StructField("phone", StringType(), True),
    ])
}

import json
import os

# Save each schema into a separate file in a package structure
base_path = "/mnt/data/cpg_distributor_schemas"
os.makedirs(base_path, exist_ok=True)

for table_name, schema in schemas.items():
    path = os.path.join(base_path, f"{table_name}_schema.json")
    with open(path, "w") as f:
        f.write(schema.json())

base_path  # Return the folder path containing all schema files
