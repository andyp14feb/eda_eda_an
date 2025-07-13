# stats/profile_missing.py
import pandas as pd
from eda_core.utils.logger_utils import setup_logger

logger = setup_logger("profile_missing")

def profile_missing(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """
    📘 Function: profile_missing

    Description:
        Profiles missing values for each column in the DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        threshold (float): Threshold for flagging high missing percentage.

    Returns:
        pd.DataFrame: Summary with columns:
            - column
            - missing
            - missing_pct
            - all_missing (bool)
            - high_missing (bool)
    """
    logger.info("Entering function profile_missing()")

    try:
        total_rows = len(df)
        missing_counts = df.isnull().sum()
        missing_pct = missing_counts / total_rows

        result = pd.DataFrame({
            "column": df.columns,
            "missing": missing_counts.values,
            "missing_pct": missing_pct.values,
            "all_missing": missing_counts == total_rows,
            "high_missing": missing_pct > threshold
        })

        logger.info(f"✅ Profiled missing data for {len(df.columns)} columns")
        return result

    except Exception as e:
        logger.error(f"❌ Failed to profile missing data: {e}")
        return pd.DataFrame(columns=[
            "column", "missing", "missing_pct", "all_missing", "high_missing"
        ])
