import os
import json
import hashlib
import pandas as pd
from datetime import datetime
from eda_core.utils.logger_utils import setup_logger
from eda_core.io.save_output import get_output_subfolder

logger = setup_logger("persist_metadata")

def calculate_hash(df: pd.DataFrame) -> str:
    """
    🧮 Calculates a hash of the DataFrame content.
    Uses SHA-1 for fast and consistent fingerprinting.
    """
    try:
        hash_val = hashlib.sha1(pd.util.hash_pandas_object(df, index=True).values).hexdigest()
        return hash_val
    except Exception as e:
        logger.error(f"Failed to compute hash: {e}")
        return ""

def persist_run_metadata(df: pd.DataFrame, original_filename) -> None:
    """
    💾 Save profiling metadata to JSON log.

    Args:
        df (pd.DataFrame): DataFrame that was analyzed
        output_path (str): Where to store the JSON log
    """
    try:
        output_path = get_output_subfolder(original_filename, "stats")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        metadata = {
            "hash": calculate_hash(df),
            "rows": len(df),
            "columns": len(df.columns),
            "run_at": datetime.now().isoformat(timespec='seconds')
        }

        with open((output_path + '/' + 'table_profile.json'), "w") as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"📦 Metadata persisted to {output_path}")

    except Exception as e:
        logger.error(f"❌ Failed to persist metadata: {e}")

def serialize_profile(profile: list[dict],original_filename) -> None:
    """
    💾 Saves column profile data to JSON.

    Args:
        profile (list[dict]): Output from table_profile()
        output_path (str): Path to save JSON file
    """
    try:
        output_path = get_output_subfolder(original_filename, "stats")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open((output_path + '/' + 'colum_profile.json'), "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)

        logger.info(f"📊 Column profile saved to {output_path}")
    except Exception as e:
        logger.error(f"❌ Failed to save column profile: {e}")
