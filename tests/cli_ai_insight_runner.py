# cli_ai_insight_runner.py
from eda_core.io.load_excel import load_excel
from eda_core.validation.validate_schema import validate_schema
from eda_core.transform.infer_dtypes import infer_dtypes
from eda_core.profile.column_report import column_report
from ai.create_ai_prompt import create_ai_prompt
from ai.llm_client import call_ollama
from pprint import pprint

def run_pipeline(file_path: str):
    print(f"📂 Loading file: {file_path}")
    df = load_excel(file_path)

    print("✅ Validating schema...")
    # validate_schema(df)

    print("🧠 Inferring data types...")
    # df = infer_dtypes(df)
    df, _ = infer_dtypes(df)

    print("📊 Running column report...")
    profile = column_report(df)

    print("🧾 Creating prompt...")
    prompt = create_ai_prompt(profile)

    print("🤖 Calling OllamaI...")
    result = call_ollama(prompt)

    print("\n🎉 Final Insight Output:")
    print("------------------------------------------------")
    print(result)
    print("------------------------------------------------")

if __name__ == "__main__":
    run_pipeline("sample_source/blahblah.xlsx")
