from langchain_ibm import WatsonxLLM
from app.config import Config
from app.models import get_model_config


MODEL_CACHE = {}


def get_llm(model_key: str):
    """
    Return a cached WatsonxLLM instance for the selected model.
    """

    if model_key in MODEL_CACHE:
        return MODEL_CACHE[model_key]

    model_config = get_model_config(model_key)

    params = {
        "temperature": Config.DEFAULT_TEMPERATURE,
        "max_new_tokens": Config.DEFAULT_MAX_NEW_TOKENS,
    }

    llm = WatsonxLLM(
        model_id=model_config["model_id"],
        url=Config.WATSONX_URL,
        apikey=Config.WATSONX_APIKEY,
        project_id=Config.WATSONX_PROJECT_ID,
        params=params,
    )

    MODEL_CACHE[model_key] = llm

    return llm