import time
from llms.groq_api import call_groq
from llms.ollama_api import call_ollama
from llms.together_api import call_together
from utils.logger import log_to_bigquery
from evaluators.judge import select_best_response
from llms.config import get_model_config
from utils.human_feedback import ask_human_for_feedback
from utils.prompt_router import route_prompt
from utils.validator import validate_model_response
def run_local(prompt):
    config = get_model_config()
    enabled_models = route_prompt(prompt)
    responses = {}
    latency_info = {}
    error_info = {}
    for model in enabled_models:
        print(f"🔹 Calling {model.upper()}...")
        call_fn = {
            "groq": call_groq,
            "ollama": call_ollama,
            "together": call_together
        }.get(model)
        if call_fn:
            start = time.time()
            try:
                resp = call_fn(prompt)
                if validate_model_response(resp):
                    responses[model] = resp
                else:
                    responses[model] = "[Invalid or empty response]"
            except Exception as e:
                responses[model] = f"Error: {str(e)}"
                error_info[model] = str(e)
            latency_info[model] = round(time.time() - start, 2)
    selected_model = ask_human_for_feedback(prompt, responses)
    if selected_model:
        best_model = selected_model
        best_response = responses[selected_model]
        print(f" Human picked: {best_model}")
    else:
        best_model, best_response, _ = select_best_response(prompt, responses)
    try:
        log_to_bigquery(prompt, responses, best_model, latency_info, error_info)
        print(" Logged to BigQuery.")
    except Exception as e:
        print(f"Logging failed: {e}")
    print("\n Responses Displayed: ")
    for model, response in responses.items():
        print(f"\n🔹 {model.upper()}:\n{response.strip()[:1000]}")
    print("\nBest Response:")
    print(f" [{best_model}] → {best_response.strip()[:1000]}")

if __name__ == "__main__":
    prompt = input("Enter prompt: ")
    run_local(prompt)
