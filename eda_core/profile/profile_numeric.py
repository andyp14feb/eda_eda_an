# stats/profile_numeric.py
import numpy as np
import pandas as pd
from eda_core.utils.logger_utils import setup_logger

logger = setup_logger("profile_numeric")

def profile_numeric(series: pd.Series) -> dict:
    """
    📘 Function: profile_numeric

    Description:
        Computes summary statistics for numeric data: min, max, mean, median,
        standard deviation, IQR, missing count, and outlier count.

    Parameters:
        series (pd.Series): A numeric pandas Series.

    Returns:
        dict: A dictionary of computed statistics.
    """
    logger.info(f"Entering function profile_numeric() → {series.name}")

    try:
        data = series.dropna()
        stats = {
            "column": series.name,
            "dtype": str(series.dtype),
            "count": len(data),
            "missing": series.isnull().sum(),
            "missing_pct": float(series.isnull().mean()),

            "mean": float(data.mean()),
            "std": float(data.std()),
            "min": float(data.min()),
            "p25": float(data.quantile(0.25)),
            "median": float(data.median()),
            "p75": float(data.quantile(0.75)),
            "max": float(data.max()),

            "iqr": float(data.quantile(0.75) - data.quantile(0.25)),
        }

        # Detect outliers using IQR method
        lower = stats["p25"] - 1.5 * stats["iqr"]
        upper = stats["p75"] + 1.5 * stats["iqr"]
        stats["outliers"] = int(((data < lower) | (data > upper)).sum())

        logger.info(f"✅ Profiled {series.name}: mean={stats['mean']}, outliers={stats['outliers']}")
        return stats

    except Exception as e:
        logger.error(f"❌ Failed to profile column {series.name}: {e}")
        return {
            "column": series.name,
            "dtype": str(series.dtype),
            "error": str(e)
        }
