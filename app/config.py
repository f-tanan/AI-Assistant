import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # IBM Watsonx credentials
    WATSONX_APIKEY = os.getenv("WATSONX_APIKEY")
    WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
    WATSONX_URL = os.getenv("WATSONX_URL")

    # Model IDs
    LLAMA_MODEL_ID = "meta-llama/llama-3-2-11b-vision-instruct"
    GRANITE_MODEL_ID = "ibm/granite-4-h-small"
    MISTRAL_MODEL_ID = "mistralai/mistral-small-3-1-24b-instruct-2503"

    # Default generation parameters
    DEFAULT_TEMPERATURE = 0.2
    DEFAULT_MAX_NEW_TOKENS = 300