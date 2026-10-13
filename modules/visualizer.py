"""
Visualization module for the sales data analysis pipeline.
Creates and saves category wise sales and monthly sales charts.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

DEFAULT_OUTPUT_DIR=Path("outputs/charts")

def create_visualizations(df,output_dir=DEFAULT_OUTPUT_DIR,):
    """
    Create and save two sales charts.
    Parameters:df(pandas.DataFrame):Valid sales records.
    output_dir(str or Path):Directory for chart files.
    Returns:tuple:Paths of the saved chart images.
    """
    required_columns=[
        "category",
        "order_date",
        "quantity",
        "unit_price",
    ]
    missing_columns=[
        column
        for column in required_columns
        if column not in df.columns
    ]
    if missing_columns:
        raise ValueError(f"Missing required columns:{missing_columns}")
    if df.empty:
        raise ValueError("Cannot create charts from an empty DataFrame.")

    chart_df=df.copy()

    # Calculate sales amount if it was not calculated earlier .
    if "sales_amount" not in chart_df.columns:
        chart_df["sales_amount"]=(chart_df["quantity"]*chart_df["unit_price"])

    output_dir=Path(output_dir)
    output_dir.mkdir(parents=True,exist_ok=True)

    category_path=output_dir/"category_sales.png"
    monthly_path=output_dir/"monthly_sales.png"

    # Chart 1 : Category-wise sales.
    category_sales=(chart_df.groupby("category")["sales_amount"].sum().sort_values(ascending=False))

    plt.figure(figsize=(9,5))
    category_sales.plot(kind="bar")
    plt.title("Category-wise Sales")
    plt.xlabel("Category")
    plt.ylabel("Sales Amount")
    plt.xticks(rotation=45,ha="right")
    plt.tight_layout()
    plt.savefig(category_path,dpi=150)
    plt.close()

    # Chart 2 : Monthly sales trend.
    chart_df["order_date"]=pd.to_datetime(chart_df["order_date"],errors="coerce")
    dated_df=chart_df.dropna(subset=["order_date"]).copy()
    dated_df["month"]=(dated_df["order_date"].dt.to_period("M").astype(str))

    monthly_sales=(dated_df.groupby("month")["sales_amount"].sum().sort_index())
    if monthly_sales.empty:
        raise ValueError("No valid order dates are available for the monthly chart.")

    plt.figure(figsize=(9,5))
    monthly_sales.plot(kind="line",marker="o")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales Amount")
    plt.xticks(rotation=45,ha="right")
    plt.grid(True,alpha=0.3)
    plt.tight_layout()
    plt.savefig(monthly_path,dpi=150)
    plt.close()

    print(f"Category chart saved to:{category_path}")
    print(f"Monthly chart saved to:{monthly_path}")

    return category_path,monthly_path

if __name__=="__main__":
    print("Visualizer module is ready.")
