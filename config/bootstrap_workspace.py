# Define configuration parameters
catalog = "main"
schema = "ecommerce"
volume = "bronze"
# Create catalog, schema, and volume
spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {catalog}.{schema}.{volume}")

# Set catalog for session
spark.sql(f"USE CATALOG {catalog}")
print(f"Initialized catalog: {catalog}, schema: {schema}, volume: {volume}")