from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
import autogen

print("Autogen Version: ",autogen.__version__)
print("Get Model Client:")

from dotenv import load_dotenv
import os
from loguru import logger

load = load_dotenv()

model = os.getenv("model")
openrouter_api_key = os.getenv("openrouter_api_key")
base_url = os.getenv("base_url")

logger.info(
    f"Using OpenRouter Model: {model}"
)

def get_model_client():

    

    return OpenAIChatCompletionClient(
        model=model,
        api_key=openrouter_api_key,
        base_url=base_url,
        max_tokens=1024,
        temperature=0.0,

        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "unknown",
            "structured_output": True
        }
    )