import os
import json

def get_secret(secret_name):
    platform = os.getenv("PLATFORM", "databricks")

    if platform == "databricks":
        return os.getenv(secret_name)
    
    elif platform == "gcp":
        from google.cloud import secretmanager
        client = secretmanager.SecretManagerServiceClient()
        project_id = os.getenv("GCP_PROJECT")
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    
    elif platform == "azure":
        from azure.identity import DefaultAzureCredential
        from azure.keyvault.secrets import SecretClient
        key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME")
        KVUri = f"https://{key_vault_name}.vault.azure.net"
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=KVUri, credential=credential)
        return client.get_secret(secret_name).value

    else:
        raise ValueError("Unsupported platform")
