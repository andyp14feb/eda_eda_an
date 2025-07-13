# # eda_eda_an/ai/llm_client.py

# """
# llm_client.py
# Author: Andy x ChatGPT

# Description:
# Provides an interface to communicate with OpenAI's LLM using the latest SDK format (openai>=1.0.0).
# """

from openai import OpenAI
import os
import time
from eda_core.utils.logger_utils import get_logger
from dotenv import load_dotenv

load_dotenv()

# Logger setup
logger = get_logger("llm_client")

# Load your API key securely from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_openai(prompt: str, model: str = "gpt-4o", max_retries: int = 3) -> str:
    """
    Sends a prompt to OpenAI and retrieves the completion.

    Parameters:
        prompt (str): The user prompt to send.
        model (str): The OpenAI model to use (default: "gpt-4o").
        max_retries (int): Retry limit for API call in case of failure.

    Returns:
        str: Model's response content.
    """
    logger.info(f"🧠 Entering call_openai() with model={model}")

    for attempt in range(1, max_retries + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert data analyst."},
                    {"role": "user", "content": prompt}
                ]
            )

            result = response.choices[0].message.content
            logger.info(f"✅ OpenAI response received successfully.")
            return result

        except Exception as e:
            logger.error(f"⚠️ OpenAI call failed (attempt {attempt}):\n\n{e}")
            time.sleep(2 * attempt)  # Exponential backoff

    return "AI response could not be retrieved."
