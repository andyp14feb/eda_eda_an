import pandas as pd
import hashlib
import os
from datetime import datetime
from eda_core.profile.column_report import column_report
from eda_core.utils.logger_utils import setup_logger

logger = setup_logger(__name__)


def get_file_hash(file_path):
    """Generate a SHA-256 hash for the file."""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        logger.warning(f"Could not hash file {file_path}: {e}")
        return None

def table_summary(df: pd.DataFrame, file_path: str = None) -> dict:
    logger.info("🧾 Generating table-level profile summary...")  

    summary = {
        "timestamp": datetime.now().isoformat(),
        "row_count": df.shape[0],
        "column_count": df.shape[1],
        "column_types": df.dtypes.value_counts().to_dict(),
        "missing_cells": int(df.isnull().sum().sum()),
        "missing_pct": round(df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100, 2),
        "source_file": file_path
    }

    # return {
    #     "row_count": int(df.shape[0]),
    #     "column_count": int(df.shape[1]),
    #     "missing_pct": float(df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100),
    #     "total_outliers": 0,  # Or use actual count from your outlier detector
    #     "source_file": file_path
    # }    

    if file_path:
        summary["file_name"] = os.path.basename(file_path)
        summary["file_size_kb"] = round(os.path.getsize(file_path) / 1024, 2)
        summary["file_hash"] = get_file_hash(file_path)

    logger.info(f"✅ Table profile created: {summary}")
    return summary

# eda_core/profile/table_profile.py



def table_profile(df: pd.DataFrame, source_filename) -> list[dict]:
    """
    📘 Function: table_profile

    Description:
        Generate a full table-level profile by compiling individual
        column reports using the column_report() function.

    Parameters:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        List[dict]: Full profile containing all column stats and insights.
    """
    logger.info("📊 Entering function table_profile()")

    try:
        profile = column_report(df,source_filename)
        logger.info(f"✅ Completed table profiling with {len(profile)} columns")
        return profile
    except Exception as e:
        logger.error(f"❌ Error in table_profile(): {e}")
        return []

