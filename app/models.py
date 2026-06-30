AVAILABLE_MODELS = {
    "watsonx_granite": {
        "display_name": "IBM Watsonx Granite",
        "provider": "watsonx",
        "model_id": "ibm/granite-4-h-small",
    },
    "watsonx_llama": {
        "display_name": "IBM Watsonx Llama",
        "provider": "watsonx",
        "model_id": "meta-llama/llama-3-3-70b-instruct",
    },
    "openai_gpt": {
        "display_name": "OpenAI GPT",
        "provider": "openai",
        "model_id": "gpt-4o-mini",
    },
}


def get_available_models():
    return [
        {
            "key": key,
            "display_name": value["display_name"],
            "provider": value["provider"],
            "model_id": value["model_id"],
        }
        for key, value in AVAILABLE_MODELS.items()
    ]


def is_valid_model(model_key: str) -> bool:
    return model_key in AVAILABLE_MODELS