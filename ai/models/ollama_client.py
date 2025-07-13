# # eda_eda_an/ai/llm_client.py

# """
# llm_client.py
# Author: Andy x ChatGPT

# Description:
# Provides an interface to communicate with OpenAI's LLM using the latest SDK format (openai>=1.0.0).
# """

import time
import logging

from eda_core.utils.logger_utils import get_logger
from dotenv import load_dotenv
import os

import requests


load_dotenv()


logger = get_logger(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:14b")

def call_ollama(prompt: str, MODEL = OLLAMA_MODEL ) -> str:
    logger.info(f"🤖 Entering call_ollama() with model={MODEL}")
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response", "[No response text]")
    except Exception as e:
        logger.error(f"💥 Failed to query Ollama: {e}")
        return "[Ollama Error]"


