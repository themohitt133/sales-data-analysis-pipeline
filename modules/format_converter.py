"""
Format converter for the Sales Data Analysis Pipeline.
Saves a Pandas DataFrame in CSV and Parquet formats.
"""
from pathlib import Path
import pandas as pd

DEFAULT_CSV_PATH=Path( "data/processed/cleaned_sales.csv")
DEFAULT_PARQUET_PATH=Path("data/processed/cleaned_sales.parquet")   

def convert_formats(df,csv_path=DEFAULT_CSV_PATH,parquet_path=DEFAULT_PARQUET_PATH):
    """
    Save a DataFrame as CSV and Parquet.
    Parameters:df(pandas.DataFrame):Data to save.
    csv_path(str or path):CSV destination.
    Returns:tuple:Paths of the saved CSV and Parquet files.
    """
    if not isinstance(df,pd.DataFrame):
        raise TypeError("Input must be a Pandas DataFrame.")
    if df.empty:
        raise ValueError("Cannot export an empty DataFrame.")
    csv_path=Path(csv_path)
    parquet_path=Path(parquet_path)

    # Create parent directories if necessary .
    csv_path.parent.mkdir(parents=True,exist_ok=True,)
    parquet_path.parent.mkdir(parents=True,exist_ok=True,)

    # Save both formats without the DataFrame index.
    df.to_csv(csv_path,index=False)
    df.to_parquet(parquet_path,index=False,engine="pyarrow",)

    print(f"CSV saved to: {csv_path}")
    print(f"Parquet saved to:{parquet_path}")
    print(f"Exported rows: {len(df)}")

    return csv_path,parquet_path

if __name__=="__main__":
    print("Format Converter module is ready.")


    