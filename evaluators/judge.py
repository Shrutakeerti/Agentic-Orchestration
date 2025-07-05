from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

def select_best_response(prompt, responses):
    """
    Select best LLM response using cosine similarity with the prompt.
    Returns: (best_model, best_response, score)
    """
    prompt_embedding = model.encode(prompt, convert_to_tensor=True)
    similarity_scores = {}

    for model_name, response in responses.items():
        if response.strip():
            response_embedding = model.encode(response, convert_to_tensor=True)
            similarity = util.cos_sim(prompt_embedding, response_embedding)
            similarity_scores[model_name] = (response, similarity.item())

    best_model = max(similarity_scores.items(), key=lambda x: x[1][1])  
    return best_model[0], best_model[1][0], best_model[1][1]
