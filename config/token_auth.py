# used if in GCP platform
# from pyspark.sql import SparkSession

# # Use the built-in Spark session
# spark = SparkSession.getActiveSession()

# if spark is None:
#     raise Exception("No active Spark session found; ensure the notebook is running on a cluster")

# print("Using built-in Spark session")
spark.sql("CREATE CATALOG IF NOT EXISTS main")
spark.sql("USE CATALOG main")
print("Using catalog: main")
