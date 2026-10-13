""" 
Outlier handling module for the Sales Data Analysis Pipeline.
This module flags records with non-positive quantity or price,saves an invalid-record report,and returns valid sales data.
"""
from pathlib import Path
import pandas as pd

DEFAULT_REPORT_PATH=Path(
    "outputs/reports/outlier_report.csv"
)

def handle_outliers(df,report_path=DEFAULT_REPORT_PATH):
    """
    Separate invalid sales records from valid records.
    Parameters:
    df(pandas.DataFrame):Cleaned sales data.
    report_path(str or Path):Destination for the report.
    Returns:
    tuple:valid_df(pandas.DataFrame):Record suitable for analysis.
    outlier_report(pandas.DataFrame):Invalid records and reasons.
    """
    required_columns=[
        "order_id",
        "quantity",
        "unit_price"
    ]
    missing_column=[
        column for column in required_columns
        if column not in df.columns
    ]
    if missing_column:
        raise ValueError(
            f"Missing required columns:{missing_column}"
        )
    # Identify invalid values
    invalid_quatity=df["quantity"]<=0
    invalid_price=df["unit_price"]<=0
    # A record is invalid if either condition is true
    invalid_mask=invalid_quatity | invalid_price

    # Copy invalid records for reporting 
    outlier_report=df.loc[invalid_mask,["order_id","quantity","unit_price"],].copy()

    
    # Build a clear reason for each invalid record
    issues = []

    for index, row in outlier_report.iterrows():
        reasons = []

        if row["quantity"] <= 0:
            reasons.append("quantity must be greater than zero")

        if row["unit_price"] <= 0:
            reasons.append("unit_price must be greater than zero")

        issues.append("; ".join(reasons))

    outlier_report["issue"] = issues


    # Keep only records that passed both checks
    valid_df=df.loc[-invalid_mask].copy()

    # Create the report directory if it does not exist
    report_path=Path(report_path) 
    report_path.parent.mkdir(parents=True,exist_ok=True,)

    # Save the report , including headers if it is empty
    outlier_report.to_csv(report_path,index=False,)

    print(f"Input records:{len(df)}")
    print(f"Invalid records:{len(outlier_report)}")
    print(f"Valid records:{len(valid_df)}")
    print(f"Outlier report saved to:{report_path}")

    return valid_df,outlier_report

if __name__=="__main__":
    print("Outlier Handler module is ready.")
