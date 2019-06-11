import json
from google.cloud import storage

def lambda_handler(event, context):
    storage_client = storage.Client.from_service_account_json(
        'gcp.json')

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)
