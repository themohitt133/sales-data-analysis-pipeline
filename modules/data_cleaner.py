"""
Data cleaning module for the Sales Data Analysis Pipeline.
This module validates and cleans the DataFrame loaded from the raw sales data files.
"""
import pandas as pd
REQUIRED_COLUMNS=[
    "order_id",
    "order_date",
    "product",
    "category",
    "quantity",
    "unit_price",
    "region"
]
def clean_data(df):
    """
    Clean and validate the raw sales DataFrame.
    Parameters:
    df(pandas.DataFrame):Raw sales data.
    Returns:
    pandas.DataFrame:
    Cleaned sales data.
    """
    cleaned_df=df.copy()
    # 1. Normalize column names 
    cleaned_df.columns=(
        cleaned_df.columns
        .str .strip() # space remove karta hai
        .str .lower() # uppercase to lowercase
    )
    # 2. Check required columns
    missing_columns=[
        column for column in REQUIRED_COLUMNS
        if column not in cleaned_df.columns
    ]
    if missing_columns:
        raise ValueError(f"Missing required columns:{missing_columns}")
    # 3. Remove exact duplicate rows 
    cleaned_df=cleaned_df.drop_duplicates()

    # 4. Convert numeric columns
    cleaned_df["quantity"]=pd.to_numeric(
        cleaned_df["quantity"],
        errors="coerce"
    )
    cleaned_df["unit_price"]=pd.to_numeric(
        cleaned_df["unit_price"],
        errors="coerce"
    )
    # 5. Convert date column
    cleaned_df["order_date"]=pd.to_datetime(
        cleaned_df["order_date"],
        errors="coerce"
    )
    # 6. Handle missing region
    cleaned_df["region"]=cleaned_df["region"].fillna("unknown")

    # 7. Remove rows with missing critical fields
    critical_columns=[
        "order_id",
        "product",
        "category",
        "quantity",
        "unit_price"
    ]
    cleaned_df=cleaned_df.dropna(subset=critical_columns)
    return cleaned_df

if __name__=="__main__":
    print("Data Cleaner module is ready.")
