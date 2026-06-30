from app.models import get_model_config


SYSTEM_PROMPT = "You are a helpful AI assistant. Answer clearly and practically."


def build_prompt(model_key: str, user_message: str) -> str:
    model_config = get_model_config(model_key)
    prompt_style = model_config["prompt_style"]

    if prompt_style == "llama":
        return build_llama_prompt(user_message)

    if prompt_style == "granite":
        return build_granite_prompt(user_message)

    if prompt_style == "mistral":
        return build_mistral_prompt(user_message)

    return user_message


def build_llama_prompt(user_message: str) -> str:
    """
    Central place for Llama prompt formatting.

    Do not blindly add special tokens here unless the Watsonx model endpoint
    requires raw prompt-template formatting.
    """
    return f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nAssistant:"


def build_granite_prompt(user_message: str) -> str:
    """
    Central place for Granite prompt formatting.

    IBM Granite 4 has its own chat-template behavior. Keep this centralized.
    """
    return f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nAssistant:"


def build_mistral_prompt(user_message: str) -> str:
    """
    Central place for Mistral prompt formatting.

    Mistral instruct models often use instruction formatting, but do not force
    tokens unless required by the Watsonx serving API.
    """
    return f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nAssistant:"


def generate_response(model: str, message: str) -> str:
    prompt = build_prompt(model_key=model, user_message=message)

    # Temporary response.
    # Next step: send `prompt` to the selected Watsonx model through LangChain.
    return f"Temporary response using model '{model}' with prompt:\n\n{prompt}"