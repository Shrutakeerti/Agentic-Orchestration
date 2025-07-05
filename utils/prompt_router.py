def route_prompt(prompt: str) -> list:
    prompt = prompt.lower()
    if any(x in prompt for x in ["math", "equation", "solve", "calculate"]):
        return ["groq"] 
    elif "translate" in prompt:
        return ["ollama"]  
    elif len(prompt) > 300:
        return ["together"]  
    elif "code" in prompt or "debug" in prompt:
        return ["groq", "together"]  
    else:
        return ["groq", "ollama", "together"]
