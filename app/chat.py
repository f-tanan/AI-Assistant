def generate_response(model: str, message: str) -> str:
    """
    Temporary chat function.

    Later, this function will call the selected LangChain model.
    For now, it only returns a dummy response.
    """

    return f"Temporary response from {model}: you said '{message}'"