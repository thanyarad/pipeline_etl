from pyspark.sql.types import *

# Retailer Customer Schema
retailer_customer_schema = StructType([
    StructField("customer_id", IntegerType(), True),
    StructField("customer_name", StringType(), True),
    StructField("registration_date", DateType(), True),
    StructField("is_active", BooleanType(), True),
    StructField("gender", StringType(), True),
    StructField("latest_activity_date", DateType(), True),
    StructField("no_of_sales_activities", IntegerType(), True),
    StructField("age", IntegerType(), True),
    StructField("address", StringType(), True),
    StructField("location_id", IntegerType(), True),
    StructField("email", StringType(), True),
    StructField("phone", StringType(), True)
])

# Customer Orders
retailer_customer_order_schema = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("order_date", DateType(), True),
    StructField("employee_id", IntegerType(), True),
    StructField("store_id", IntegerType(), True),
    StructField("order_status", StringType(), True),
    StructField("total_amount", FloatType(), True),
    StructField("currency", StringType(), True),
    StructField("payment_method", StringType(), True),
    StructField("channel", StringType(), True)
])

# Order Items
retailer_customer_order_items_schema = StructType([
    StructField("order_item_id", IntegerType(), True),
    StructField("order_id", IntegerType(), True),
    StructField("product_id", IntegerType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("unit_price", FloatType(), True),
    StructField("total_price", FloatType(), True)
])

# Customer Invoices
retailer_customer_invoice_schema = StructType([
    StructField("invoice_id", IntegerType(), True),
    StructField("order_id", IntegerType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("invoice_date", DateType(), True),
    StructField("total_items", IntegerType(), True),
    StructField("gross_amount", FloatType(), True),
    StructField("discount_amount", FloatType(), True),
    StructField("tax_amount", FloatType(), True),
    StructField("net_amount", FloatType(), True),
    StructField("payment_method", StringType(), True),
    StructField("status", StringType(), True)
])

# Products
retailer_products_schema = StructType([
    StructField("product_id", IntegerType(), True),
    StructField("upc", StringType(), True),
    StructField("gtin", StringType(), True),
    StructField("sku_id", StringType(), True),
    StructField("department", StringType(), True),
    StructField("category", StringType(), True),
    StructField("brand", StringType(), True),
    StructField("product_title", StringType(), True),
    StructField("description", StringType(), True),
    StructField("retail_price", FloatType(), True),
    StructField("unit_measurement", StringType(), True),
    StructField("expiration_days", IntegerType(), True),
    StructField("release_date", DateType(), True),
    StructField("item_status", StringType(), True)
])

# Inventory
retailer_stock_schema = StructType([
    StructField("stock_id", IntegerType(), True),
    StructField("store_id", IntegerType(), True),
    StructField("product_id", IntegerType(), True),
    StructField("supplier_source_id", IntegerType(), True),
    StructField("quantity_on_hand", IntegerType(), True),
    StructField("reorder_level", IntegerType(), True),
    StructField("reorder_quantity", IntegerType(), True),
    StructField("last_restock_date", DateType(), True),
    StructField("safety_stock_level", IntegerType(), True),
    StructField("stock_status", StringType(), True)
])

# Supplier
retailer_supplier_schema = StructType([
    StructField("supplier_id", IntegerType(), True),
    StructField("supplier_name", StringType(), True),
    StructField("company_name", StringType(), True),
    StructField("last_activity_date", DateType(), True),
    StructField("no_of_associated_deals", IntegerType(), True),
    StructField("total_open_deal_value", FloatType(), True),
    StructField("rating", FloatType(), True),
    StructField("email", StringType(), True),
    StructField("phone", StringType(), True),
    StructField("location_id", IntegerType(), True),
    StructField("address", StringType(), True)
])

# Supplier Sources
retailer_supplier_sources_schema = StructType([
    StructField("supplier_source_id", IntegerType(), True),
    StructField("supplier_id", IntegerType(), True),
    StructField("source_id", IntegerType(), True),
    StructField("is_active", BooleanType(), True)
])

# Supplier Source Info
retailer_supplier_source_schema = StructType([
    StructField("source_id", IntegerType(), True),
    StructField("source_code", StringType(), True),
    StructField("name", StringType(), True),
    StructField("is_pickup_location", BooleanType(), True),
    StructField("address", StringType(), True),
    StructField("location_id", IntegerType(), True),
    StructField("email", StringType(), True),
    StructField("phone", StringType(), True)
])

# Supplier Purchases
retailer_supplier_purchase_schema = StructType([
    StructField("supplier_purchase_id", IntegerType(), True),
    StructField("store_id", IntegerType(), True),
    StructField("supplier_source_id", IntegerType(), True),
    StructField("order_date", DateType(), True),
    StructField("expected_delivery_date", DateType(), True),
    StructField("order_status", StringType(), True),
    StructField("total_amount", FloatType(), True),
    StructField("currency", StringType(), True)
])

# Purchase Items
retailer_supplier_purchase_items_schema = StructType([
    StructField("supplier_purchase_item_id", IntegerType(), True),
    StructField("supplier_purchase_id", IntegerType(), True),
    StructField("product_id", IntegerType(), True),
    StructField("stock_id", IntegerType(), True),
    StructField("manufacturer_id", IntegerType(), True),
    StructField("upc", StringType(), True),
    StructField("quantity_ordered", IntegerType(), True),
    StructField("unit_cost", FloatType(), True),
    StructField("total_price", FloatType(), True)
])

# Supplier Invoice
retailer_supplier_invoice_schema = StructType([
    StructField("supplier_invoice_id", IntegerType(), True),
    StructField("supplier_order_id", IntegerType(), True),
    StructField("invoice_date", DateType(), True),
    StructField("amount_due", FloatType(), True),
    StructField("tax_amount", FloatType(), True),
    StructField("discount", FloatType(), True),
    StructField("total_payable", FloatType(), True),
    StructField("payment_status", StringType(), True),
    StructField("payment_method", StringType(), True),
    StructField("due_date", DateType(), True)
])

# Store
retailer_store_schema = StructType([
    StructField("store_id", IntegerType(), True),
    StructField("store_name", StringType(), True),
    StructField("store_type", StringType(), True),
    StructField("location_id", IntegerType(), True),
    StructField("address", StringType(), True),
    StructField("contact_number", StringType(), True),
    StructField("email", StringType(), True),
    StructField("is_active", BooleanType(), True)
])

# Store Manager
retailer_store_manager_schema = StructType([
    StructField("manager_id", IntegerType(), True),
    StructField("manager_name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("phone", StringType(), True),
    StructField("store_id", IntegerType(), True),
    StructField("job_title", StringType(), True),
    StructField("department", StringType(), True),
    StructField("start_date", DateType(), True),
    StructField("is_active", BooleanType(), True)
])

# Store Employee
retailer_store_employee_schema = StructType([
    StructField("employee_id", IntegerType(), True),
    StructField("employee_name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("phone", StringType(), True),
    StructField("role", StringType(), True),
    StructField("store_id", IntegerType(), True),
    StructField("reports_to_id", IntegerType(), True),
    StructField("hire_date", DateType(), True),
    StructField("is_active", BooleanType(), True)
])

# Location
location_schema = StructType([
    StructField("location_id", IntegerType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("country", StringType(), True)
])
