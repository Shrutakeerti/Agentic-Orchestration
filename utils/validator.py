def validate_model_response(response):
    if not response:
        return False
    if len(response.strip()) < 10:
        return False
    return True
