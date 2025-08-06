import os
import yaml

with open("config/env.yaml") as f:
    config = yaml.safe_load(f)

platform = config.get("platform")

if platform == "databricks":
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {config['catalog']}.{config['schema']}")
    spark.sql(f"CREATE VOLUME IF NOT EXISTS {config['catalog']}.{config['schema']}.{config['volume_name']}")

elif platform == "gcp":
    # Create GCS buckets and BigQuery datasets
    from google.cloud import storage, bigquery
    client = bigquery.Client()
    dataset_id = f"{config['project_id']}.{config['schema']}"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = config["region"]
    client.create_dataset(dataset, exists_ok=True)

elif platform == "azure":
    # Create ADLS container and Synapse schema
    # Requires Azure SDK setup
    pass
