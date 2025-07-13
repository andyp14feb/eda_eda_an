# validate_schema.py
import pandas as pd
from eda_core.utils.logger_utils import setup_logger

logger = setup_logger("validate_schema")

# def validate_schema(df: pd.DataFrame, rules: dict) -> dict:
#     """
#     📘 Function: validate_schema

#     Description:
#         Validates the DataFrame based on user-defined rules like max size and header presence.

#     Parameters:
#         df (pd.DataFrame): The DataFrame to validate.
#         rules (dict): Dictionary of validation rules (e.g., max_rows, max_cols, require_headers).

#     Returns:
#         dict: {
#             "ok": bool,
#             "errors": list of error messages
#         }

#     Example:
#         rules = {
#             "max_rows": 1_000_000,
#             "max_cols": 100,
#             "require_headers": True
#         }
#     """
#     logger.info("Entering function validate_schema()")
#     errors = []

#     # Rule: Check max rows
#     max_rows = rules.get("max_rows")
#     if max_rows and df.shape[0] > max_rows:
#         msg = f"Too many rows: {df.shape[0]} (max {max_rows})"
#         logger.warning(msg)
#         errors.append(msg)

#     # Rule: Check max columns
#     max_cols = rules.get("max_cols")
#     if max_cols and df.shape[1] > max_cols:
#         msg = f"Too many columns: {df.shape[1]} (max {max_cols})"
#         logger.warning(msg)
#         errors.append(msg)

#     # Rule: Header row required (basic check: columns must not be unnamed)
#     if rules.get("require_headers", True):
#         unnamed = [col for col in df.columns if str(col).lower().startswith("unnamed")]
#         if unnamed:
#             msg = f"Missing or invalid headers in columns: {unnamed}"
#             logger.warning(msg)
#             errors.append(msg)

#     # Rule: Check for fully empty DataFrame
#     if df.empty:
#         msg = "DataFrame is completely empty."
#         logger.warning(msg)
#         errors.append(msg)

#     result = {
#         "ok": len(errors) == 0,
#         "errors": errors
#     }

#     logger.info("Validation result: " + ("PASS" if result["ok"] else "FAIL"))
#     return result


def validate_schema(df: pd.DataFrame, rules: dict = None) -> dict:
    logger.info("Entering function validate_schema()")
    errors = []

    # ✅ Safe fallback
    if rules is None:
        rules = {}

    # Rule: Check max rows
    max_rows = rules.get("max_rows")
    if max_rows and df.shape[0] > max_rows:
        msg = f"Too many rows: {df.shape[0]} (max {max_rows})"
        logger.warning(msg)
        errors.append(msg)

    # Rule: Check max columns
    max_cols = rules.get("max_cols")
    if max_cols and df.shape[1] > max_cols:
        msg = f"Too many columns: {df.shape[1]} (max {max_cols})"
        logger.warning(msg)
        errors.append(msg)

    # Rule: Header row required (basic check: columns must not be unnamed)
    if rules.get("require_headers", True):
        unnamed = [col for col in df.columns if str(col).lower().startswith("unnamed")]
        if unnamed:
            msg = f"Missing or invalid headers in columns: {unnamed}"
            logger.warning(msg)
            errors.append(msg)

    # Rule: Check for fully empty DataFrame
    if df.empty:
        msg = "DataFrame is completely empty."
        logger.warning(msg)
        errors.append(msg)

    result = {
        "ok": len(errors) == 0,
        "errors": errors
    }

    logger.info("Validation result: " + ("PASS" if result["ok"] else "FAIL"))
    return result