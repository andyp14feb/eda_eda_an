import os
import argparse
import pandas as pd
from typing import Iterator
from eda_core.utils.logger_utils import setup_logger



logger = setup_logger("load_excel")

def load_excel(file_path: str, chunksize: int | None = None) -> pd.DataFrame | Iterator[pd.DataFrame]:
    """
    📘 Function: load_excel

    Description:
        Loads an Excel file (.xlsx or .xls) using pandas.
        - If chunksize is None, loads the entire sheet into memory.
        - If chunksize is provided, returns an iterator over DataFrame chunks.

    Parameters:
        file_path (str): Full path to the Excel file to load.
        chunksize (int | None): Number of rows per chunk. If None, loads full DataFrame.

    Returns:
        pd.DataFrame: If chunksize is None.
        Iterator[pd.DataFrame]: If chunksize is specified.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not a valid Excel format.
        IOError: If an error occurs during reading.

    Usage Example:
        df = load_excel("data.xlsx")
        for chunk in load_excel("large_file.xlsx", chunksize=100000):
            process(chunk)
    """
    logger.info("Entering function load_excel()")

    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.lower().endswith((".xlsx", ".xls")):
        logger.error("Unsupported file format")
        raise ValueError("Only .xlsx or .xls files are supported.")

    try:
        if chunksize is None:
            df = pd.read_excel(file_path, engine="openpyxl")
            logger.info(f"Successfully loaded file into DataFrame with shape {df.shape}")
            return df
        else:
            logger.info(f"Returning chunked reader with chunksize={chunksize}")
            return pd.read_excel(file_path, engine="openpyxl", chunksize=chunksize)

    except Exception as e:
        logger.exception("Error reading Excel file")
        raise IOError(f"Error reading Excel file: {e}")

def main():
    """
    🧪 Manual CLI Test Interface

    Description:
        Command-line entry point to test load_excel().
        Accepts an Excel file path and an optional --chunksize flag.
        Prints shape of the full DataFrame or of each chunk.

    CLI Example:
        python load_excel.py ./mydata.xlsx
        python load_excel.py ./bigfile.xlsx --chunksize 100000
    """
    parser = argparse.ArgumentParser(
        description="📂 Load Excel file for Auto-EDA. Supports full load or chunked read for large files."
    )
    parser.add_argument("file_path", type=str, help="Path to the Excel file (.xlsx or .xls)")
    parser.add_argument(
        "--chunksize",
        type=int,
        default=None,
        help="Optional. Read the file in chunks of N rows for large files."
    )

    args = parser.parse_args()
    logger.info("Running main() in load_excel")

    print(f"🔍 Loading file: {args.file_path}")
    try:
        result = load_excel(args.file_path, chunksize=args.chunksize)
        if isinstance(result, Iterator):
            for i, chunk in enumerate(result):
                print(f"🔹 Chunk {i + 1}: shape = {chunk.shape}")
        else:
            print(f"✅ Loaded DataFrame shape: {result.shape}")
    except Exception as e:
        logger.info(f"❌ Error: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
