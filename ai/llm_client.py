# ai/llm_client.py

from ai.models.ollama_client import call_ollama
from ai.models.openai_client import call_openai
# from ai.models.gemini_client import call_gemini
# from ai.models.groq_client import call_groq

def query_model(prompt: str, model: str = "ollama") -> str:
    """
    🧠 query_model – Selects and uses the correct model backend.

    Parameters:
        prompt (str): Prompt to send.
        model (str): One of ["ollama", "openai"]

    Returns:
        str: AI-generated response text.
    """
    if model == "ollama":
        return call_ollama(prompt)
    elif model == "openai":
        return call_openai(prompt)
    # elif model == "gemini":
    #     return call_gemini(prompt)
    # elif model == "groq":
    #     return call_groq(prompt)
    else:
        raise ValueError(f"Unsupported model: {model}")
