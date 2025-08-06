import os

def detect_platform():
    if os.getenv("DATABRICKS_RUNTIME_VERSION"):
        return "databricks"
    elif os.getenv("GOOGLE_CLOUD_PROJECT"):
        return "gcp"
    elif os.getenv("AZURE_HTTP_USER_AGENT"):
        return "azure"
    else:
        return "unknown"
