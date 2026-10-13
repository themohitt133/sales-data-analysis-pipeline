
"""
Main entry point for the Sales Data Analysis Pipeline.

Accepts an input CSV path and coordinates the full pipeline.
"""

import argparse

from modules.data_loader import load_csv
from modules.data_cleaner import clean_data
from modules.outlier_handler import handle_outliers
from modules.analysis_engine import analyze_sales
from modules.format_converter import convert_formats
from modules.visualizer import create_visualizations


DEFAULT_INPUT_PATH = "data/raw/sales_data.csv"


def main(input_path):
    """Run the complete sales data pipeline."""

    print("=" * 55)
    print("SALES DATA ANALYSIS & PROCESSING PIPELINE")
    print("=" * 55)
    print(f"Input file: {input_path}")

    # Step 1: Load raw data.
    print("\n[1/6] Loading raw sales data...")
    raw_df = load_csv(input_path)
    print(f"Raw records loaded: {len(raw_df)}")

    # Step 2: Clean data.
    print("\n[2/6] Cleaning sales data...")
    cleaned_df = clean_data(raw_df)
    print(f"Records after cleaning: {len(cleaned_df)}")

    # Step 3: Handle invalid records.
    print("\n[3/6] Handling invalid records...")
    valid_df, outlier_report = handle_outliers(cleaned_df)

    if valid_df.empty:
        raise ValueError(
            "No valid sales records remain after cleaning "
            "and validation."
        )

    # Step 4: Analyze sales.
    print("\n[4/6] Analyzing sales data...")
    results = analyze_sales(valid_df)
    kpis = results["kpis"]

    print("\n--- SALES KPIs ---")
    print(f"Total sales: {kpis['total_sales']:.2f}")
    print(f"Unique orders: {kpis['total_orders']}")
    print(f"Total units sold: {kpis['total_units']}")
    print(
        "Average order value: "
        f"{kpis['avg_order_value']:.2f}"
    )

    print("\n--- CATEGORY-WISE SALES ---")
    print(results["category_sales"].to_string(index=False))

    print("\n--- CATEGORY-WISE UNITS ---")
    print(results["category_units"].to_string(index=False))

    print("\n--- REGION-WISE SALES ---")
    print(results["region_sales"].to_string(index=False))

    print("\n--- MONTHLY ORDER COUNTS ---")
    print(results["monthly_orders"].to_string(index=False))
    print("\n--- MONTHLY SALES ---")
    print(results["monthly_sales"].to_string(index=False))

    # Step 5: Export valid data.
    print("\n[5/6] Exporting sales data...")
    csv_path, parquet_path = convert_formats(valid_df)

    # Step 6: Create charts.
    print("\n[6/6] Creating visualizations...")
    category_chart, monthly_chart = (
        create_visualizations(valid_df)
    )

    # Final summary.
    print("\n" + "=" * 55)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 55)

    print(f"Raw records: {len(raw_df)}")
    print(f"Cleaned records: {len(cleaned_df)}")
    print(f"Valid records: {len(valid_df)}")
    print(f"Invalid records reported: {len(outlier_report)}")

    print("\nGenerated files:")
    print(f"CSV: {csv_path}")
    print(f"Parquet: {parquet_path}")
    print("Outlier report: outputs/reports/outlier_report.csv")
    print(f"Category chart: {category_chart}")
    print(f"Monthly chart: {monthly_chart}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the Sales Data Analysis Pipeline."
    )

    parser.add_argument(
        "--input",
        default=None,
        help="Path to the input sales CSV file.",
    )

    args = parser.parse_args()

    if args.input:
        input_path = args.input
    else:
        print("\nSALES DATA ANALYSIS & PROCESSING PIPELINE")
        print("-" * 45)
        print("Enter the path of your CSV file.")
        print("Press Enter to use the default file:")
        print(f"Default: {DEFAULT_INPUT_PATH}")

        user_path = input("\nCSV path: ").strip()
        input_path = user_path or DEFAULT_INPUT_PATH

    try:
        main(input_path)
    except (FileNotFoundError, ValueError) as error:
        print(f"\nERROR: {error}")
