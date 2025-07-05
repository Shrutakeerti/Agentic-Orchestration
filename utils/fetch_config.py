from google.cloud import storage
import json

def load_remote_config():
    client = storage.Client()
    bucket = client.bucket("agentic-configs")
    blob = bucket.blob("config.json")
    data = blob.download_as_text()
    return json.loads(data)
