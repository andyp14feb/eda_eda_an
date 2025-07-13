# ai/create_ai_prompt.py
import json
from eda_core.utils.logger_utils import setup_logger

logger = setup_logger("create_ai_prompt")

def create_ai_prompt(profile_data: list[dict], tone: str = "neutral") -> str:
    """
    📘 Function: create_ai_prompt

    Description:
        Converts profiling results into a natural language prompt for LLMs.

    Parameters:
        profile_data (list[dict]): Output from column_report()
        tone (str): Optional tone ('neutral', 'casual', 'executive', etc.)

    Returns:
        str: The full prompt ready to send to LLM
    """
    logger.info("🧠 Entering create_ai_prompt()")

    try:
        # print('======================================')
        # print('======================================')
        # print(f'profile_data : {profile_data}')
        # print('======================================')
        
        profile_json = json.dumps(profile_data, indent=2)
        
        # print('======================================')
        # print(f'profile_json : {profile_json}')
        # print('======================================')
        # print('======================================')

        prompt = f"""
You are a smart data analyst AI assistant.

Tone: {tone}

The user uploaded a dataset, and the following is the profiling summary for each column.
Your job is to:
1. Give 3–5 short but deep insights about this data
2. Mention if there's anything odd, missing, or worth investigating
3. Suggest next steps for the user (e.g. visualization, cleaning, validation)

Output should be plain English, easy to understand, and structured.

DATA PROFILE JSON:
{profile_json}
        """.strip()

        logger.info("✅ Prompt successfully created")
        return prompt

    except Exception as e:
        logger.error(f"❌ Failed to create prompt: {e}")
        return "Prompt creation failed."
