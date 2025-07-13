# infer_dtypes.py
import pandas as pd
from eda_core.utils.logger_utils import setup_logger

logger = setup_logger("infer_dtypes")

def infer_dtypes(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    📘 Function: infer_dtypes

    Description:
        Attempts to infer better data types for each column in the DataFrame.
        Especially useful for converting strings to datetime, integers, or booleans.

    Parameters:
        df (pd.DataFrame): The input DataFrame with raw types (e.g., from Excel).

    Returns:
        Tuple[pd.DataFrame, dict]: (updated DataFrame, conversion_log)

    conversion_log = {
        "column_name": "original_type → new_type"
    }

    Notes:
        - Does not modify the original DataFrame.
        - Uses pandas smart inference (e.g., `to_numeric`, `to_datetime`, etc.)
    """
    logger.info("Entering function infer_dtypes()")

    df_clean = df.copy()
    conversion_log = {}

    for col in df.columns:
        original_type = str(df[col].dtype)
        new_col = df[col]

        # Try convert to numeric
        try:
            converted = pd.to_numeric(df[col], errors='raise')
            df_clean[col] = converted
            new_type = str(converted.dtype)
            if new_type != original_type:
                conversion_log[col] = f"{original_type} → {new_type}"
                logger.info(f"{col}: {conversion_log[col]}")
                continue
        except Exception:
            pass

        # Try convert to datetime
        try:
            converted = pd.to_datetime(df[col], errors='raise')
            df_clean[col] = converted
            new_type = str(converted.dtype)
            if new_type != original_type:
                conversion_log[col] = f"{original_type} → {new_type}"
                logger.info(f"{col}: {conversion_log[col]}")
                continue
        except Exception:
            pass

        # Try convert to boolean
        try:
            if set(df[col].dropna().unique()).issubset({0, 1, "0", "1", "True", "False", True, False}):
                converted = df[col].map(lambda x: str(x).lower() in ["1", "true"])
                df_clean[col] = converted
                new_type = str(converted.dtype)
                if new_type != original_type:
                    conversion_log[col] = f"{original_type} → {new_type}"
                    logger.info(f"{col}: {conversion_log[col]}")
                    continue
        except Exception:
            pass

        # Fallback if no conversion worked
        conversion_log[col] = f"{original_type} → {original_type}"
        logger.info(f"{col}: Unchanged ({original_type})")

    logger.info(f"Inferred {sum(1 for v in conversion_log.values() if '→' in v and not v.endswith('→ ' + v.split('→')[-1]))} column types.")
    return df_clean, conversion_log
