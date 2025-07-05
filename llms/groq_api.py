from dotenv import load_dotenv
load_dotenv()
import requests
import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
def call_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    body = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }
    res = requests.post(url, headers=headers, json=body)
    return res.json()["choices"][0]["message"]["content"]
