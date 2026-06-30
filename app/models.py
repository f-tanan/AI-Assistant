from app.config import Config


AVAILABLE_MODELS = {
    "llama": {
        "display_name": "Llama 3.2 11B Vision Instruct",
        "provider": "watsonx",
        "model_id": Config.LLAMA_MODEL_ID,
        "prompt_style": "llama",
    },
    "granite": {
        "display_name": "IBM Granite 4H Small",
        "provider": "watsonx",
        "model_id": Config.GRANITE_MODEL_ID,
        "prompt_style": "granite",
    },
    "mistral": {
        "display_name": "Mistral Small 3.1 24B Instruct",
        "provider": "watsonx",
        "model_id": Config.MISTRAL_MODEL_ID,
        "prompt_style": "mistral",
    },
}


def get_available_models():
    return [
        {
            "key": key,
            "display_name": value["display_name"],
            "provider": value["provider"],
            "model_id": value["model_id"],
            "prompt_style": value["prompt_style"],
        }
        for key, value in AVAILABLE_MODELS.items()
    ]


def is_valid_model(model_key: str) -> bool:
    return model_key in AVAILABLE_MODELS


def get_model_config(model_key: str) -> dict:
    return AVAILABLE_MODELS[model_key]