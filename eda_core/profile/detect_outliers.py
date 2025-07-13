# eda_core/profile/detect_outliers.py
import pandas as pd
import numpy as np
from eda_core.utils.logger_utils import setup_logger

logger = setup_logger("detect_outliers")

def detect_outliers(series: pd.Series, method: str = "iqr", z_threshold: float = 3.0) -> dict:
    """
    📘 Function: detect_outliers

    Description:
        Detects outliers in a numeric series using either IQR or Z-score method.

    Parameters:
        series (pd.Series): The numeric series to analyze.
        method (str): 'iqr' or 'zscore'.
        z_threshold (float): Z-score threshold, used only if method == 'zscore'.

    Returns:
        dict: {
            'column': column_name,
            'method': 'iqr' or 'zscore',
            'outlier_count': int,
            'outlier_idx': list of indices,
            'lower_bound': float,
            'upper_bound': float
        }
    """
    logger.info(f"Entering function detect_outliers() → {series.name}")

    data = series.dropna()
    colname = series.name

    try:
        if method == "iqr":
            q1 = data.quantile(0.25)
            q3 = data.quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

        elif method == "zscore":
            mean = data.mean()
            std = data.std()
            lower = mean - z_threshold * std
            upper = mean + z_threshold * std

        else:
            raise ValueError("Unsupported method. Use 'iqr' or 'zscore'.")

        outlier_mask = (data < lower) | (data > upper)
        outlier_idx = list(data[outlier_mask].index)
        outlier_count = len(outlier_idx)

        logger.info(f"✅ Outliers in {colname}: {outlier_count} using {method.upper()}")

        return {
            "column": colname,
            "method": method,
            "outlier_count": outlier_count,
            "outlier_idx": outlier_idx,
            "lower_bound": float(lower),
            "upper_bound": float(upper)
        }

    except Exception as e:
        logger.error(f"❌ Failed to detect outliers in {colname}: {e}")
        return {
            "column": colname,
            "method": method,
            "error": str(e)
        }
