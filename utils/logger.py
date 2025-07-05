from google.cloud import bigquery
from datetime import datetime
import json
from llms.config import get_model_config
def log_to_bigquery(prompt, responses, best_response, latency_info=None, error_info=None):
    client = bigquery.Client()
    table_id = "agentic-architecture-464807.agentic.logs"

    model_config = get_model_config()
    model_versions = json.dumps({k: v.get("model", "") for k, v in model_config.items()})

    row = [{
        "prompt": prompt,
        "responses": json.dumps(responses),
        "best": best_response,
        "timestamp": datetime.utcnow().isoformat(),
        "model_versions": model_versions,
        "latency_info": json.dumps(latency_info or {}),
        "error_info": json.dumps(error_info or {})
    }]
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("prompt", "STRING"),
            bigquery.SchemaField("responses", "STRING"),
            bigquery.SchemaField("best", "STRING"),
            bigquery.SchemaField("timestamp", "TIMESTAMP"),
            bigquery.SchemaField("model_versions", "STRING"),
            bigquery.SchemaField("latency_info", "STRING"),
            bigquery.SchemaField("error_info", "STRING"),
        ],
        write_disposition="WRITE_APPEND",
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )
    import io
    buffer = io.StringIO('\n'.join([json.dumps(r) for r in row]))
    job = client.load_table_from_file(buffer, table_id, job_config=job_config)
    job.result()
    print("Logged to BigQuery.")
