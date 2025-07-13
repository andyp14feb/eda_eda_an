# eda_core/io/save_output.py

import os
import json
from datetime import datetime
from eda_core.utils.logger_utils import setup_logger

logger = setup_logger("save_output")


def get_base_filename(file_path: str) -> str:
    """
    Extracts the base filename (without extension) from a full file path.

    Example:
        "sample_source/blahblah.xlsx" → "blahblah"

    Args:
        file_path (str): Full file path.

    Returns:
        str: Base filename without extension.
    """
    return os.path.splitext(os.path.basename(file_path))[0]


def get_output_subfolder(source_filename: str, subfolder: str) -> str:
    """
    Returns an output subfolder path like 'outputs/blahblah/stats/'.
    Creates the directory if not exists.
    """
    base_name = os.path.splitext(os.path.basename(source_filename))[0]
    folder_path = os.path.join("outputs", base_name, subfolder)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def save_json(data: dict, file_prefix: str = "insight", original_filename: str ="") -> str:
    """
    💾 Save final AI-generated insight to a JSON file.

    Parameters:
        data (dict): Data to be saved.
        output_dir (str): Directory where the file will be saved.
        file_prefix (str): Prefix for the file name.

    Returns:
        str: Full path to the saved file.
    """
    try:
        output_dir = get_output_subfolder(original_filename, "insights")
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.splitext(os.path.basename(original_filename))[0]
        base_name = filename.replace(".xlsx", "").replace(".json", "").replace(".xls", "")        
        file_path = os.path.join(output_dir, f"{file_prefix}_{timestamp}_{base_name}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"✅ Insight saved to {file_path}")
        return file_path

    except Exception as e:
        logger.error(f"❌ Failed to save insight JSON: {e}")
        return ""

# eda_core/io/save_output.py — extend with:
def save_table_insight(insight_text: str, original_filename: str = "") -> str:
    try:
        output_dir = get_output_subfolder(original_filename, "insights")
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.splitext(os.path.basename(original_filename))[0]
        safe_name = filename.replace("/", "_").replace("\\", "_")
        output_file = os.path.join(output_dir, f"table_insight_{timestamp}_{safe_name}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"table_insight": insight_text}, f, indent=2, ensure_ascii=False)
        logger.info(f"📝 Saved table insight to {output_file}")
        return output_file
    except Exception as e:
        logger.error(f"❌ Failed to save table insight: {e}")
        return ""

def save_markdown(markdown_text: str, original_filename: str) -> str:
    """
    💾 Save rendered markdown report into the correct output/docs folder
    based on the original Excel source file name.

    Parameters:
        markdown_text (str): Rendered markdown content
        original_filename (str): Full path to the source Excel file (e.g., 'sample_source/blahblah.xlsx')

    Returns:
        str: Full file path to the saved markdown file
    """
    try:
        # Get docs output directory like: outputs/blahblah/docs
        doc_output_dir = get_output_subfolder(original_filename, "docs")
        os.makedirs(doc_output_dir, exist_ok=True)

        # Save file as report.md
        output_path = os.path.join(doc_output_dir, f"report_{original_filename}.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_text)

        logger.info(f"✅ Markdown report saved to {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"❌ Failed to save markdown report: {e}")
        return ""