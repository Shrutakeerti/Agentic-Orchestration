import base64
import json
import time
from llms.config import get_model_config
from llms.groq_api import call_groq
from llms.ollama_api import call_ollama
from llms.together_api import call_together
from evaluators.judge import select_best_response
from utils.logger import log_to_bigquery
from utils.validator import validate_model_response
def run_agents(event, context):
    try:
        data = json.loads(base64.b64decode(event['data']).decode("utf-8"))
        prompt = data.get("prompt", "").strip()
        if not prompt:
            raise ValueError("Prompt missing in request data.")

        config = get_model_config()
        responses = {}
        latency_info = {}
        error_info = {}

        for model, call_fn in {
            "groq": call_groq,
            "together": call_together,
            "ollama": call_ollama
        }.items():
            if config.get(model, {}).get("enabled"):
                print(f"🔹 Calling {model.upper()}...")
                start = time.time()
                try:
                    response = call_fn(prompt)
                    if validate_model_response(response):
                        responses[model] = response
                    else:
                        responses[model] = "[Invalid or empty response]"
                except Exception as e:
                    responses[model] = f"Error: {str(e)}"
                    error_info[model] = str(e)
                latency_info[model] = round(time.time() - start, 2)

        if not responses:
            raise Exception("No valid model responses.")

        best_model, best_response, _ = select_best_response(prompt, responses)

        try:
            log_to_bigquery(prompt, responses, best_model, latency_info, error_info)
            print("Logged to BigQuery.")
        except Exception as e:
            print(f"BigQuery logging failed: {e}")

        print(" All responses collected successfully.")
        return {
            "prompt": prompt,
            "responses": responses,
            "best_model": best_model,
            "best_response": best_response
        }

    except Exception as e:
        print(f"Error in run_agents: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    fake_event = {
        "data": base64.b64encode(json.dumps({
            "prompt": "What is Agentic AI?"
        }).encode("utf-8")).decode("utf-8")
    }

    run_agents(fake_event, None)
