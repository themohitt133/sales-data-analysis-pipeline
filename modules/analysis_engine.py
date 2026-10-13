"""
Analysis engine for the Sales Data Analysis Pipeline.
Calculates sales KPIs and grouped business summaaries. 
"""
import pandas as pd

def analyze_sales(df):
    """
    Calculate sales KPIs and grouped summaries.
    Parameters: df(pandas.DataFrame): Valid sales records from the Outlier Handler.
    Returns: dict:KPIs and grouped analysis DataFrames.
    """
    required_columns=[
        "order_id",
        "order_date",
        "category",
        "quantity",
        "unit_price",
        "region",
    ]
    missing_columns=[
        column
        for column in required_columns
        if column not in df.columns
    ]
    if missing_columns:
        raise ValueError(f"Missing required columns:{missing_columns}")
    if df.empty:
        raise ValueError("Cannot analyze sales because the DataFrame is empty.")
    
    # Work on a a copy so the input DataFrame is not modified.
    analysis_df=df.copy()

    # Ensure dates are usable for mothly analysis.
    analysis_df["order_date"]=pd.to_datetime(
        analysis_df["order_date"],
        errors="coerce",
    )

    # Calculate sales amount for every valid records.
    analysis_df["sales_amount"]=(
        analysis_df["quantity"]*analysis_df["unit_price"]
    )

    # Overall business KPIs.
    total_sales=analysis_df["sales_amount"].sum()
    total_orders=analysis_df["order_id"].nunique()
    total_units=analysis_df["quantity"].sum()

    avg_order_value=(
        total_sales/total_orders
        if total_orders>0
        else 0
    )

    kpis={
        "total_sales":float(total_sales),
        "total_orders":int(total_orders),
        "total_units":int(total_units),
        "avg_order_value":float(avg_order_value),
    }

    
    # Category-wise sales amount.
    category_sales = (
        analysis_df.groupby("category", as_index=False)
        .agg(total_sales=("sales_amount", "sum"))
        .sort_values("total_sales", ascending=False)
    )

    # Category-wise units sold.
    category_units = (
        analysis_df.groupby("category", as_index=False)
        .agg(total_units=("quantity", "sum"))
        .sort_values("total_units", ascending=False)
    )


    # Exclude invalid/missing dates from monthly summaries.
    dated_df=analysis_df.dropna(subset=["order_date"]).copy()
    dated_df["month"]=(
        dated_df["order_date"].dt.to_period("M").astype(str)
    )

    # Monthly sales.
    monthly_sales=(
        dated_df.groupby("month",as_index=False)
        .agg(total_sales=("sales_amount","sum"))
        .sort_values("month")
    )

    # Monthly unique orders.
    monthly_orders=(
        dated_df.groupby("month",as_index=False)
        .agg(total_orders=("order_id","nunique"))
        .sort_values("month")
    )

    # Region wise sales.
    region_sales=(
        analysis_df.groupby("region",as_index=False)
        .agg(total_sales=("sales_amount","sum"))
        .sort_values("total_sales",ascending=False)
    )

    
    return {
        "kpis": kpis,
        "category_sales": category_sales,
        "category_units": category_units,
        "monthly_sales": monthly_sales,
        "monthly_orders": monthly_orders,
        "region_sales": region_sales,
    }


if __name__=="__main__":
    print("Analysis Engine module is ready.")