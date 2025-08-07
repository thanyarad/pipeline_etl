from pyspark.sql import SparkSession

# Initialize Spark
spark = SparkSession.builder.getOrCreate()

# Set catalog and database (schema)
spark.sql("USE CATALOG cpg_industry")
spark.sql("USE SCHEMA bronze")

# Base path where all JSON files are stored
base_path = "/Volumes/cpg_industry/cpg_data/data"

# List of folders and corresponding JSON tables
folders_and_tables = {
    "cpg_consumer": [
        "cpg_consumer",
        "cpg_consumer_order",
        "cpg_order_items",
        "cpg_consumer_invoice"
    ],
    "cpg_inventory": [
        "cpg_inventory",
        "cpg_product"
    ],
    "cpg_distributor": [
        "cpg_distributor_purchases",
        "cpg_distributor_purchase_items",
        "cpg_distributor_invoice",
        "cpg_distributor"
    ]
}

# Loop through folders and tables
for folder, tables in folders_and_tables.items():
    for table in tables:
        input_path = f"{base_path}{folder}/{table}.json"
        print(f"Reading from: {input_path}")
        
        # Read JSON
        df = spark.read.option("multiline", "true").json(input_path)
        
        # Write to bronze schema as Delta table
        df.write.mode("overwrite").format("delta").saveAsTable(f"bronze.{table}")
        print(f"✅ Saved to bronze.{table}")
