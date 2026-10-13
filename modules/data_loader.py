"""
Data loading module for the Sales Data Analysis Pipeline.

This module loads raw sales data from CSV and JSON files into Pandas DataFrames.
"""

import pandas as pd
from pathlib import Path


def load_csv(file_path):
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"CSV file not found: {path}\n"
            "Please check the file path and try again."
        )

    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError as exc:
        raise ValueError(
            f"CSV file is empty: {path}"
        ) from exc


def load_json(file_path):
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"JSON file not found: {path}"
        )

    return pd.read_json(path)


if __name__ == "__main__":
    print("Data Loader module is ready.")
