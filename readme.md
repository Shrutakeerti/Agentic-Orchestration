# Agentic AI Orchestration System using Google Cloud

This project implements an **Agentic AI System** that orchestrates prompts across multiple LLMs (Groq, Together, Ollama), selects the best response using evaluation logic or human feedback, and logs all results to **BigQuery**. It is built with **Google Cloud Functions**, **Pub/Sub**, and **modular LLM APIs**, supporting **hot-swapping**, **prompt routing**, and **real-time monitoring**.

---

##  Features

-  Prompt routing across multiple LLMs (Groq, Together, Ollama)
-  Config-based model enable/disable and versioning
-  Response evaluation logic (length-based + human feedback)
-  Logging to BigQuery (prompt, latency, best model, etc.)
-  Zero-downtime model hot-swapping
-  CLI-based local execution for debugging and validation
-  Cloud-native (Pub/Sub, Cloud Functions, BigQuery)

---

##  Architecture Overview

```text
[User Prompt]
     ↓
[Pub/Sub Topic: agentic-prompts]
     ↓
[Cloud Function Triggered: subscriber.py]
     ↓
[Prompt Routing (prompt_router.py)]
     ↓
[Selected LLMs: GROQ, TOGETHER, OLLAMA]
     ↓
[Response Evaluation / Human Feedback]
     ↓
[Best Response Selected]
     ↓
[Logged in BigQuery + Printed in CLI]
```


## 🛠️ Project Structure
```text
agentic-ai-orchestration/
├── cloud_functions/
│ ├── route_prompt/main.py # Pub/Sub publisher
│ └── run_agents/main.py # Cloud Function subscriber
├── llms/
│ ├── config.py # Enabled models + versions
│ ├── groq_api.py # GROQ LLM API
│ ├── together_api.py # Together API
│ └── ollama_api.py # Local Ollama API
├── utils/
│ ├── logger.py # Log results to BigQuery
│ ├── prompt_router.py # Dynamic model selection logic
│ ├── selector.py # Evaluation/Scoring function
│ └── human_feedback.py # CLI-based feedback
├── evaluators/
│ └── judge.py # Simple evaluation logic
├── local_runner.py # Local CLI interface
├── subscriber.py # Main Cloud Function logic
├── requirements.txt
├── .env # API keys and project vars
└── README.md
```

---

## Setup Instructions

### 1. Environment Setup

Create a `.env` file in the root directory:

```env
GCP_PROJECT_ID=your-gcp-project-id
GROQ_API_KEY=your-groq-key
TOGETHER_API_KEY=your-together-key
GOOGLE_APPLICATION_CREDENTIALS=cred.json
``` 
## Path to GCP service account JSON
```


##  Google Cloud Setup

```bash
gcloud pubsub topics create agentic-prompts
gcloud pubsub subscriptions create agentic-sub --topic=agentic-prompts

bq mk --table agentic.logs \
  prompt:STRING,responses:STRING,best_model:STRING,timestamp:TIMESTAMP

```

##  Install Python Requirements

```bash
pip install -r requirements.txt
```

##  How to Run

### Option 1:  Local Testing (with CLI feedback)

```bash
python local_runner.py
```

##  Option 2: Cloud Function Execution

### A. Start the Cloud Subscriber

```bash
python subscriber.py

gcloud pubsub topics publish agentic-prompts \
--message="{\"prompt\": \"Who was the first female F1 driver?\"}"
```

##  BigQuery Schema

**Table:** `agentic.logs`

| Field         | Type     | Description                             |
|---------------|----------|-----------------------------------------|
| `prompt`      | STRING   | User input prompt                       |
| `responses`   | STRING   | JSON of model outputs                   |
| `best_model`  | STRING   | Model with highest score/selected best |
| `latency_info`| RECORD   | Timing and performance data             |
| `error_info`  | RECORD   | Any error traces                        |
| `timestamp`   | TIMESTAMP| Request time                            |

---

##  Model Management and Hot-Swapping

All model configurations are managed in `llms/config.py`:

```python
"groq": {
  "enabled": True,
  "model": "llama3-70b-8192",
  "version": "v1.0"
},
"together": {
  "enabled": True,
  "model": "meta-llama/Llama-3-8b-chat-hf",
  "version": "v1.1"
},
"ollama": {
  "enabled": True,
  "model": "mistral",
  "version": "v1.1"
}
```


###  To Hot-Swap Models

1. Add a new model to `llms/config.py` with `"enabled": False`  
2. Test the model locally using:

   ```bash
   python local_runner.py
   ```


   Once validated, set `"enabled": True` → Ready for production

---

##  Monitoring and Observability

-  Logs stored in **BigQuery**
-  View **latency**, **model performance**, and **failure rates**
-  Analyze **usage patterns** over time
-  GCP **Alerting & Monitoring** *(future scope)*

---

##  Human-in-the-Loop (CLI Feedback)

In `local_runner.py`, all LLM responses are displayed for manual selection.

This supports:

-  Validating auto-selection logic  
-  Collecting human-labeled data for fine-tuning evaluation functions

---

##  Future Improvements

-  Web-based frontend for prompt submission  
-  Semantic evaluation using fine-tuned scoring models  
-  Prompt classification using a lightweight LLM  
-  GCP alerting and observability integration  
-  Web UI for human-in-the-loop feedback

---

##  License

MIT License

---

## Author 
Made by Shrutakeerti with love.


