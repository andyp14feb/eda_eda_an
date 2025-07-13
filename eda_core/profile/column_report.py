# eda_core/profile/column_report.py
import pandas as pd
from eda_core.profile.profile_numeric import profile_numeric
from eda_core.profile.profile_categorical import profile_categorical
from eda_core.profile.detect_outliers import detect_outliers
from eda_core.profile.profile_missing import profile_missing
from eda_core.utils.logger_utils import setup_logger
import json
from eda_core.plots.plot_utils import plot_numeric_hist, plot_box  # 💡 Add import at top
from eda_core.io.save_output import get_output_subfolder

logger = setup_logger("column_report")

def column_report(df: pd.DataFrame, source_filename) -> list[dict]:
    """
    📘 Function: column_report

    Description:
        Combines multiple profiling functions into a single unified
        per-column report for numeric and categorical data.

    Parameters:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        List[dict]: List of column profiles.
    """
    logger.info("📊 Entering function column_report()")

    reports = []
    missing_df = profile_missing(df).set_index("column")

    for col in df.columns:
        series = df[col]
        dtype = str(series.dtype)

        try:
            if pd.api.types.is_numeric_dtype(series):
                logger.info(f"🔢 Profiling numeric column: {col}")
                base_report = profile_numeric(series)
                outlier_info = detect_outliers(series)
                base_report.update({"outlier_count": outlier_info["outlier_count"]})

                base_report.update({
                    "outlier_method": outlier_info["method"],
                    "outlier_count": outlier_info["outlier_count"]
                })

                # 📊 Generate plots and record paths
                hist_path = plot_numeric_hist(series, col,source_filename)
                box_path = plot_box(series, col,source_filename)
                base_report.update({
                    "histogram_path": hist_path,
                    "boxplot_path": box_path
                })


            elif pd.api.types.is_string_dtype(series) or pd.api.types.is_categorical_dtype(series):
                logger.info(f"🔤 Profiling categorical column: {col}")
                base_report = profile_categorical(series)

            else:
                logger.info(f"❔ Skipped unsupported column: {col}")
                base_report = {
                    "column": col,
                    "dtype": dtype,
                    "note": "Unsupported data type"
                }

            # Add missing info to report
            if col in missing_df.index:
                base_report.update({
                    "missing": int(missing_df.loc[col, "missing"]),
                    "missing_pct": float(missing_df.loc[col, "missing_pct"]),
                    "all_missing": bool(missing_df.loc[col, "all_missing"]),
                    "high_missing": bool(missing_df.loc[col, "high_missing"]),
                })

            reports.append(base_report)

        except Exception as e:
            logger.error(f"❌ Failed to process column {col}: {e}")
            reports.append({
                "column": col,
                "dtype": dtype,
                "error": str(e)
            })

    logger.info(f"✅ Completed profiling for {len(df.columns)} columns")
    return reports


def serialize_profile(table_summary: dict, column_profiles: list[dict], file_path: str):
    """
    📦 Function: serialize_profile

    Description:
        Combines table-level summary and column-level profiles, then saves to JSON.

    Parameters:
        table_summary (dict): Overall summary of the table
        column_profiles (list[dict]): Per-column profile list
        file_path (str): Destination path for the JSON file
    """

    logger.info(f"💾 Serializing profile to {file_path}")
    data = {
        "table_summary": table_summary,
        "column_profiles": column_profiles
    }
    try:

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info("✅ Profiling data successfully written to JSON")
    except Exception as e:
        logger.error(f"❌ Failed to write profiling JSON: {e}")
