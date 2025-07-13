# test_numeric_profile.py
from io import StringIO
import pandas as pd
from eda_core.io.load_excel import load_excel
from eda_core.validation.validate_schema import validate_schema
from eda_core.transform.infer_dtypes import infer_dtypes
from eda_core.profile.profile_numeric import profile_numeric

def test_numeric_profile_from_excel(file_path: str):
    print(f"🔍 Processing file: {file_path}")

    # Load
    df = load_excel(file_path)
    print(f"✅ Loaded: {df.shape}")

    # Validate
    validation = validate_schema(df, {
        "max_rows": 1_000_000,
        "max_cols": 200,
        "require_headers": True
    })

    if not validation["ok"]:
        print("❌ Validation failed:")
        for err in validation["errors"]:
            print(" -", err)
        return

    # Infer Types
    df_inferred, log = infer_dtypes(df)
    print("🧠 Inferred Dtypes:")
    for k, v in log.items():
        print(f" - {k}: {v}")

    # Profile Numeric Columns
    numeric_cols = df_inferred.select_dtypes(include=["int64", "float64"]).columns
    print(f"📊 Found {len(numeric_cols)} numeric columns")

    results = []
    for col in numeric_cols:
        profile = profile_numeric(df_inferred[col])
        results.append(profile)

    return results


if __name__ == "__main__":
    from pprint import pprint
    result = test_numeric_profile_from_excel("./sample_source/blahblah.xlsx")
    pprint(result)
