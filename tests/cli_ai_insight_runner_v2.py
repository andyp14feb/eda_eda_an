import os
import sys

# ✅ Append root path dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from eda_core.io.load_excel import load_excel
from eda_core.validation.validate_schema import validate_schema
from eda_core.transform.infer_dtypes import infer_dtypes
from eda_core.profile.table_profile import table_summary, table_profile
from ai.create_ai_prompt import create_ai_prompt
from ai.generate_ai_insight import generate_ai_insight
from ai.generate_ai_insight import annotate_profile
import numpy as np
from eda_core.utils.persist_metadata import persist_run_metadata, serialize_profile
from eda_core.io.save_output import save_json
from eda_core.io.save_output import save_table_insight, get_base_filename
from eda_core.io.save_output import save_markdown
from eda_core.io.render_markdown import render_markdown
from datetime import datetime


def sanitize_keys(d: dict) -> dict:
    return {str(k): v for k, v in d.items()}


def sanitize_summary(summary: dict) -> dict:
    cleaned = {}
    for k, v in summary.items():
        # Fix for column_types which contains np.dtype keys
        if k == "column_types" and isinstance(v, dict):
            cleaned[k] = {str(key): int(val) for key, val in v.items()}
        elif isinstance(v, (np.integer, np.floating)):
            cleaned[k] = float(v)
        else:
            cleaned[k] = v
    return cleaned



def run_pipeline(path):
    source_filename = get_base_filename(path)

    print(f"📂 Loading file: {path}")
    df = load_excel(path)

    print("✅ Validating schema...")
    validate_schema(df, rules=None)

    print("🔍 Inferring data types...")
    df_clean, conversion_log = infer_dtypes(df)


    print("📄 Generating table summary...")
    summary = table_summary(df_clean, file_path=path)
    print("\n=== 📊 Table Summary ===")
    for k, v in summary.items():
        print(f"{k}: {v}")

    # print("\n🧠 Profiling columns... ")
    # column_profiles = table_profile(df)

    print("\n🧠 Profiling columns...")
    column_profiles = table_profile(df_clean,source_filename)

    # after column_profiles = column_report(df)
    column_profiles = annotate_profile(column_profiles, model="ollama")

    # Save profile
    serialize_profile(column_profiles,source_filename)

    # Save metadata
    persist_run_metadata(df_clean,source_filename)


    print("🪄 Generating AI prompt...")
    summary_clean = sanitize_summary(summary)
    # print('======================================')
    # print('======================================')
    # print(f'summary : {summary}')
    # print('======================================')
    # print(f'summary_clean : {summary_clean}')
    # print('======================================')
    # print('======================================')
    prompt = create_ai_prompt(summary_clean, column_profiles)

    print("🤖 Generating AI insight...")
    insight = generate_ai_insight(prompt)

    print("\n🎉 Table Insight Output:")
    print("-" * 48)
    print(insight)
    print("-" * 48)

    print("💾 Saving insight result to JSON file...")
    save_json(insight,original_filename=path)


    # 📝 Save table-level insight separately
    if isinstance(insight, dict) and insight.get("status") == "success":
        save_table_insight(
            insight_text=insight.get("insight", ""),
            original_filename=source_filename
        )
    print("📝 Table-level insight saved to JSON.")


    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_meta = {
        "source_name": source_filename,
        "created_at": created_at
    }

    md_text = render_markdown(column_profiles, summary, file_meta)
    md_path = save_markdown(md_text, original_filename=file_meta["source_name"])
    print(f"📝 Markdown file saved to outputs folder {md_path}.")



if __name__ == "__main__":
    # run_pipeline("sample_source/cupu.xlsx")
    # run_pipeline("sample_source/blahblah.xlsx")

    sample_dir = "sample_source"
    for filename in os.listdir(sample_dir):
        if filename.endswith(".xlsx"):
            filepath = os.path.join(sample_dir, filename)
            run_pipeline(filepath)