from google.cloud import pubsub_v1
import os
import json
import time
from llms.groq_api import call_groq
from llms.ollama_api import call_ollama
from llms.together_api import call_together
from evaluators.judge import select_best_response
from utils.logger import log_to_bigquery
from utils.prompt_router import route_prompt
from utils.validator import validate_model_response
from utils.human_feedback import ask_human_for_feedback 
project_id = os.getenv("GCP_PROJECT_ID")
subscription_id = "agentic-sub"
subscription_path = f"projects/{project_id}/subscriptions/{subscription_id}"
def callback(message):
    prompt = message.data.decode("utf-8")
    print(f" Received Prompt: {prompt}")
    selected_models = route_prompt(prompt)
    responses = {}
    latency_info = {}
    error_info = {}
    for model in selected_models:
        print(f"🔹 Calling {model.upper()}...")
        call_fn = {
            "groq": call_groq,
            "ollama": call_ollama,
            "together": call_together
        }.get(model)

        start = time.time()
        try:
            response = call_fn(prompt) if call_fn else None
        except Exception as e:
            response = f" Error: {str(e)}"
            error_info[model] = str(e)
        latency_info[model] = round(time.time() - start, 2)

        if validate_model_response(response):
            responses[model] = response
        else:
            print(f" Skipped invalid response from {model}")

    if not responses:
        print(" No valid responses")
        message.ack()
        return
    selected_model = ask_human_for_feedback(prompt, responses)
    if selected_model:
        best_model = selected_model
        best_response = responses[selected_model]
        print(f" Human selected: {best_model}")
    else:
        best_model, best_response, _ = select_best_response(prompt, responses)
        print(f" Auto-selected best: {best_model}")
    try:
        log_to_bigquery(prompt, responses, best_model, latency_info, error_info)
        print(" Logged to BigQuery.")
        print(f" Latency Info: {latency_info}")
        print(f"Error Info: {error_info}")
    except Exception as e:
        print(f" Logging failed: {e}")
    print("\n Responses ")
    for model, response in responses.items():
        print(f"\n🔹 {model.upper()}:\n{response.strip()[:700]}...\n")

    print(f"Best Response:\n [{best_model}] → {best_response.strip()[:700]}...\n")

    message.ack()
def main():
    subscriber = pubsub_v1.SubscriberClient()
    future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening on: {subscription_path}\n")

    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()
        print(" Stopped.")

if __name__ == "__main__":
    main()
