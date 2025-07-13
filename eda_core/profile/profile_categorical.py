# stats/profile_categorical.py
import pandas as pd
import numpy as np
from eda_core.utils.logger_utils import setup_logger
from collections import Counter

logger = setup_logger("profile_categorical")

def profile_categorical(series: pd.Series, top_k: int = 5) -> dict:
    """
    📘 Function: profile_categorical

    Description:
        Generate statistics for a categorical column such as top-k values,
        frequencies, mode, and entropy (diversity measure).

    Parameters:
        series (pd.Series): A string/categorical column
        top_k (int): Number of top frequent values to include

    Returns:
        dict: Profiling result
    """
    logger.info(f"Entering function profile_categorical() → {series.name}")
    try:
        col = series.dropna().astype(str)
        counts = col.value_counts().head(top_k)
        total = len(col)
        entropy = -sum((c / total) * np.log2(c / total) for c in counts)

        top_k_values = [
            {"value": v, "count": int(c), "pct": float(c / total)}
            for v, c in counts.items()
        ]

        result = {
            "column": series.name,
            "dtype": str(series.dtype),
            "count": int(total),
            "missing": int(series.isnull().sum()),
            "unique": int(series.nunique(dropna=True)),
            "mode": col.mode().iloc[0] if not col.mode().empty else None,
            "top_k_values": top_k_values,
            "entropy": float(entropy)
        }

        logger.info(f"✅ Profiled {series.name}: unique={result['unique']}, mode={result['mode']}")
        return result

    except Exception as e:
        logger.error(f"❌ Failed to profile column {series.name}: {e}")
        return {
            "column": series.name,
            "dtype": str(series.dtype),
            "error": str(e)
        }
