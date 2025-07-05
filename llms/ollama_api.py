import requests
import json
def call_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": True},
            stream=True
        )
        output = ""
        for line in response.iter_lines():
            if line:
                try:
                    decoded = json.loads(line.decode("utf-8"))
                    output += decoded.get("response", "")
                except json.JSONDecodeError:
                    continue
        return output.strip() if output.strip() else "Error: Ollama gave empty output."
    except Exception as e:
        return f"Error: {str(e)}"
