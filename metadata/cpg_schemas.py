from pyspark.sql.types import *

# -----------------------------
# 1. CPG Consumer
# -----------------------------
cpg_consumer_schema = StructType([
    StructField("consumer_id", StringType(), False),
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
    StructField("country", StringType(), True)
])

# -----------------------------
# 2. CPG Product
# -----------------------------
cpg_product_schema = StructType([
    StructField("product_id", StringType(), False),
    StructField("sku_id", StringType(), True),
    StructField("upc", StringType(), True),
    StructField("gtin", StringType(), True),
    StructField("product_name", StringType(), True),
    StructField("description", StringType(), True),
    StructField("department", StringType(), True),
    StructField("category", StringType(), True),
    StructField("brand", StringType(), True),
    StructField("unit_of_measurement", StringType(), True),
    StructField("retail_price", DoubleType(), True),
    StructField("unit_price", DoubleType(), True),
    StructField("release_date", DateType(), True),
    StructField("expiration_days", IntegerType(), True),
    StructField("product_status", StringType(), True)
])

# -----------------------------
# 3. CPG Consumer Order
# -----------------------------
cpg_consumer_order_schema = StructType([
    StructField("order_id", StringType(), False),
    StructField("consumer_id", StringType(), True),
    StructField("order_date", DateType(), True),
    StructField("shipping_address", StringType(), True),
    StructField("billing_address", StringType(), True),
    StructField("order_status", StringType(), True),
    StructField("total_amount", DoubleType(), True),
    StructField("payment_method", StringType(), True),
    StructField("currency", StringType(), True),
    StructField("channel", StringType(), True)
])

# -----------------------------
# 4. CPG Order Items
# -----------------------------
cpg_order_items_schema = StructType([
    StructField("order_item_id", StringType(), False),
    StructField("order_id", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("unit_price", DoubleType(), True),
    StructField("total_price", DoubleType(), True)
])

# -----------------------------
# 5. CPG Consumer Invoice
# -----------------------------
cpg_consumer_invoice_schema = StructType([
    StructField("invoice_id", StringType(), False),
    StructField("order_id", StringType(), True),
    StructField("consumer_id", StringType(), True),
    StructField("invoice_date", DateType(), True),
    StructField("total_items", IntegerType(), True),
    StructField("gross_amount", DoubleType(), True),
    StructField("discount_amount", DoubleType(), True),
    StructField("tax_amount", DoubleType(), True),
    StructField("net_amount", DoubleType(), True),
    StructField("payment_method", StringType(), True),
    StructField("invoice_status", StringType(), True)
])

# -----------------------------
# 6. CPG Inventory
# -----------------------------
cpg_inventory_schema = StructType([
    StructField("inventory_id", StringType(), False),
    StructField("product_id", StringType(), True),
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
    StructField("phone", StringType(), True)
])

# -----------------------------
# 7. CPG Distributor Purchases
# -----------------------------
cpg_distributor_purchases_schema = StructType([
    StructField("purchase_id", StringType(), False),
    StructField("order_date", DateType(), True),
    StructField("expected_delivery_date", DateType(), True),
    StructField("order_status", StringType(), True),
    StructField("total_amount", DoubleType(), True),
    StructField("currency", StringType(), True)
])

# -----------------------------
# 8. CPG Distributor Purchase Items
# -----------------------------
cpg_distributor_purchase_items_schema = StructType([
    StructField("purchase_item_id", StringType(), False),
    StructField("purchase_id", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("upc", StringType(), True),
    StructField("quantity_ordered", IntegerType(), True),
    StructField("unit_cost", DoubleType(), True),
    StructField("total_price", DoubleType(), True)
])

# -----------------------------
# 9. CPG Distributor Invoice
# -----------------------------
cpg_distributor_invoice_schema = StructType([
    StructField("invoice_id", StringType(), False),
    StructField("purchase_id", StringType(), True),
    StructField("invoice_date", DateType(), True),
    StructField("amount_due", DoubleType(), True),
    StructField("tax_amount", DoubleType(), True),
    StructField("discount", DoubleType(), True),
    StructField("total_payable", DoubleType(), True),
    StructField("payment_status", StringType(), True)
])

# -----------------------------
# 10. Distributor Inventory
# -----------------------------
# distributor_inventory_schema = StructType([
#     StructField("inventory_id", StringType(), False),
#     StructField("distributor_id", StringType(), True),
#     StructField("product_id", StringType(), True),
#     StructField("quantity_on_hand", IntegerType(), True),
#     StructField("reorder_level", IntegerType(), True),
#     StructField("reorder_quantity", IntegerType(), True),
#     StructField("last_restock_date", DateType(), True),
#     StructField("safety_stock_level", IntegerType(), True),
#     StructField("inventory_status", StringType(), True),
#     StructField("last_updated", TimestampType(), True),
#     StructField("location_code", StringType(), True),
#     StructField("location_name", StringType(), True),
#     StructField("location_type", StringType(), True),
#     StructField("location_is_active", BooleanType(), True),
#     StructField("address", StringType(), True),
#     StructField("city", StringType(), True),
#     StructField("state", StringType(), True),
#     StructField("country", StringType(), True),
#     StructField("email", StringType(), True),
#     StructField("phone", StringType(), True)
# ])

# -----------------------------
# 11. Distributor Details
# -----------------------------
cpg_distributor_schema = StructType([
    StructField("distributor_id", StringType(), False),
    StructField("distributor_name", StringType(), True),
    StructField("company_name", StringType(), True),
    StructField("last_activity_date", DateType(), True),
    StructField("no_of_associated_deals", IntegerType(), True),
    StructField("total_open_deal_value", DoubleType(), True),
    StructField("rating", DoubleType(), True),
    StructField("email", StringType(), True),
    StructField("phone", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("country", StringType(), True),
    StructField("address", StringType(), True)
])
