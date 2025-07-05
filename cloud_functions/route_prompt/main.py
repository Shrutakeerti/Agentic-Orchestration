from google.cloud import pubsub_v1
import os
import json
publisher = pubsub_v1.PublisherClient()
project_id = os.environ.get("GCP_PROJECT", "agentic-architecture-464807")
topic_path = publisher.topic_path(project_id, "agentic-prompts")

def route_prompt(request):
    req = request.get_json()
    prompt = req["prompt"]
    publisher.publish(topic_path, json.dumps({"prompt": prompt}).encode("utf-8"))
    return {"status": "queued"}, 200

