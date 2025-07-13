# ai/generate_ai_insight.py
# import json
# import pandas as pd
from eda_core.io.load_excel import load_excel
from eda_core.validation.validate_schema import validate_schema
from eda_core.transform.infer_dtypes import infer_dtypes
from eda_core.profile.column_report import column_report
from ai.llm_client import query_model  # to be created
from eda_core.utils.logger_utils import setup_logger
from ai.create_ai_prompt import create_ai_prompt

import time



logger = setup_logger("generate_ai_insight")


# ai/generate_ai_insight.py

from ai.llm_client import query_model
from eda_core.utils.logger_utils import setup_logger

logger = setup_logger("generate_ai_insight")

def generate_ai_insight(prompt: str, model: str = "ollama") -> dict:
    """
    ✨ Generates insights using the provided AI prompt.

    Parameters:
        prompt (str): The input prompt for the AI model.
        model (str): Which AI model to use (default is 'ollama').

    Returns:
        dict: AI-generated insights.
    """
    logger.info("🚀 Generating insight from prompt")

    try:
        insight = query_model(prompt=prompt, model=model)
        return {
            "status": "success",
            "insight": insight
        }

    except Exception as e:
        logger.error(f"❌ Failed in generate_ai_insight: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


# ai/generate_ai_insight.py or a new module like ai/annotator.py



def annotate_profile(column_profiles: list[dict], model: str = "ollama") -> list[dict]:
    """
    🧠 annotate_profile()

    Enhances each column profile with an AI-generated insight.

    Parameters:
        column_profiles (list[dict]): The list of column profiling results.
        model (str): Which LLM model to use: 'ollama', 'openai', etc.

    Returns:
        list[dict]: Updated column profiles with 'ai_insight' field added.
    """
    annotated = []

    for col in column_profiles:
        col_name = col.get("column", "Unknown")
        try:
            prompt = f"""
You are a data analyst. Here's a column profile:

{col}

Provide an insight, observation, or suggestion about this column.
Focus on its usefulness, data quality, patterns, or issues you observe.
            """.strip()

            response = query_model(prompt=prompt, model=model)
            col["ai_insight"] = response.strip()
            annotated.append(col)
            print(f"📝 Insight generated for column: {col_name}")

            # Add optional delay to avoid overload (especially with OpenAI)
            time.sleep(0.5)

        except Exception as e:
            print(f"⚠️ Failed to annotate column: {col_name} → {e}")
            col["ai_insight"] = f"[Error] {str(e)}"
            annotated.append(col)

    return annotated
