def select_best_response(prompt, responses):
    """
    Heuristic to select the best response from multiple LLMs.
    Default: chooses the longest coherent response.
    """
    best_model = None
    best_response = ""

    for model, response in responses.items():
        if response and len(response.strip()) > len(best_response.strip()):
            best_model = model
            best_response = response

    return best_model, best_response
