from dotenv import load_dotenv
load_dotenv()
def get_model_config():
    return {
        "groq": {
            "enabled": True,
            "model": "llama3-70b-8192",
            "version": "v1.2.0"  
        },
        "together": {
            "enabled": True,
            "model": "meta-llama/Llama-3-8b-chat-hf",
            "version": "v0.1.7"  
        },
        "ollama": {
            "enabled": True,
            "model": "mistral",
            "version": "v2.0.3"  
        }
    }
