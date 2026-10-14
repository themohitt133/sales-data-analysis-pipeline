# Sales Data Analysis & Processing Pipeline

A modular Python-based data engineering project that loads sales data, cleans and validates records, analyzes sales performance, exports processed data into CSV and Parquet formats, and generates visual reports.

## Project Overview

This project demonstrates a basic end-to-end data processing pipeline using Python, Pandas, NumPy, Matplotlib, and PyArrow.

It transforms raw sales data into structured, analysis-ready data and produces summaries that help understand sales performance across product categories, months, and regions.

## Features

- Load sales data from a CSV file.
- Accept a custom input CSV path through an interactive prompt or command-line argument.
- Clean column names and convert data types.
- Remove exact duplicate records.
- Handle missing and invalid values.
- Identify invalid sales records, including non-positive quantities and prices.
- Generate sales KPIs and category-wise, monthly, and region-wise summaries.
- Export processed data to CSV and Parquet formats.
- Generate category-wise sales and monthly sales charts.
- Produce an invalid-record report.
- Handle common input errors with readable error messages.

## Technology Stack

- **Python** — pipeline logic and modular programming
- **Pandas** — data loading, cleaning, transformation, grouping, and aggregation
- **NumPy** — numerical computing
- **Matplotlib** — data visualization
- **PyArrow** — Parquet file support
- **CSV, JSON, Parquet** — data formats used or explored in the project
- **Git and GitHub** — version control and project hosting

## Project Structure

```text
sales-data-analysis-pipeline/
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── modules/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_cleaner.py
│   ├── outlier_handler.py
│   ├── analysis_engine.py
│   ├── format_converter.py
│   └── visualizer.py
├── data/
│   ├── raw/
│   │   ├── sales_data.csv
│   │   └── sales_data.json
│   └── processed/
│       ├── cleaned_sales.csv
│       └── cleaned_sales.parquet
├── outputs/
│   ├── charts/
│   │   ├── category_sales.png
│   │   └── monthly_sales.png
│   └── reports/
│       └── outlier_report.csv
└── screenshots/
    ├── pipeline-success.png
    ├── category-sales-chart.png
    └── monthly-sales-chart.png
    
```

## Pipeline Architecture

```text
Raw Sales CSV
     |
     v
Data Loader
     |
     v
Data Cleaner
     |
     v
Outlier Handler
     |
     +----------------------+
     |                      |
     v                      v
Valid Sales Data      Invalid-Record Report
     |
     +----------------------+
     |                      |
     v                      v
Analysis Engine       Format Converter
     |                      |
     v                      v
Sales Summaries       CSV and Parquet
     |
     v
Visualizer
     |
     v
Sales Charts
```

## Module Responsibilities

| Module | Responsibility |
|---|---|
| `data_loader.py` | Loads input data and checks for common file errors. |
| `data_cleaner.py` | Normalizes column names, converts data types, removes exact duplicates, and handles missing critical values. |
| `outlier_handler.py` | Identifies invalid quantity and price values, separates valid records, and generates a report. |
| `analysis_engine.py` | Calculates sales KPIs and category-wise, monthly, and region-wise summaries. |
| `format_converter.py` | Exports processed data to CSV and Parquet. |
| `visualizer.py` | Generates category-wise sales and monthly sales charts. |
| `main.py` | Coordinates the pipeline from input selection through processing and output generation. |

## Requirements

- Python installed on your system
- pip
- A terminal such as Windows PowerShell or the VS Code integrated terminal

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/themohitt133/sales-data-analysis-pipeline.git
cd sales-data-analysis-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the pipeline from the project root directory.

### Interactive mode

```bash
python main.py
```

The program prompts for the path to a CSV file. Press **Enter** to use the default input:

```text
data/raw/sales_data.csv
```

### Specify an input file

```bash
python main.py --input "data/raw/sales_data.csv"
```

You can also provide another CSV file:

```bash
python main.py --input "data/raw/another_sales.csv"
```

The specified file must exist at the given path.

### View available command-line options

```bash
python main.py --help
```

## Input Data Schema

The input CSV is expected to contain these columns:

| Column | Description |
|---|---|
| `order_id` | Identifier for an order |
| `order_date` | Date of the order |
| `product` | Product name |
| `category` | Product category |
| `quantity` | Number of units ordered |
| `unit_price` | Price per unit |
| `region` | Sales region |

The pipeline calculates:

```text
sales_amount = quantity × unit_price
```

## Data Cleaning and Validation

The pipeline applies the following rules:

- Trims whitespace from column names and converts them to lowercase.
- Checks that required columns are present.
- Removes exact duplicate rows.
- Converts `quantity` and `unit_price` to numeric values.
- Converts `order_date` to datetime values.
- Replaces missing region values with `Unknown`.
- Removes records missing critical fields such as order ID, product, category, quantity, or unit price.
- Identifies records where quantity or unit price is zero or negative.
- Excludes identified invalid sales records from the valid dataset used by the downstream pipeline.
- Excludes missing or invalid dates from monthly summaries.
- Does not automatically remove high positive values solely because they appear unusually large.

The invalid-record report records the affected orders and the associated validation issue.

## Sales Analysis

The analysis module calculates the following metrics and summaries:

### Key Performance Indicators (KPIs)

- **Total Sales:** Sum of calculated sales amounts.
- **Unique Orders:** Number of distinct order IDs.
- **Total Units Sold:** Sum of quantities.
- **Average Order Value:** Total sales divided by the number of unique orders.

### Category Analysis

- Category-wise sales amount.
- Category-wise units sold.

### Time-Based Analysis

- Monthly sales amount.
- Monthly unique order count.

### Regional Analysis

- Total sales by region.

Monthly summaries exclude records with missing or invalid order dates. Other summaries follow the valid dataset passed to the analysis module.

## Generated Outputs

The pipeline generates the following files when it runs successfully:

| Output | Purpose |
|---|---|
| `data/processed/cleaned_sales.csv` | Processed sales data in CSV format |
| `data/processed/cleaned_sales.parquet` | Processed sales data in Parquet format |
| `outputs/reports/outlier_report.csv` | Report of invalid sales records |
| `outputs/charts/category_sales.png` | Category-wise sales visualization |
| `outputs/charts/monthly_sales.png` | Monthly sales visualization |

The `screenshots/` directory contains screenshots captured during project execution for documentation and demonstration.

## Error Handling

The pipeline handles common errors such as:

- Missing input files.
- Empty CSV files.
- Missing required columns.
- Empty datasets passed to the analysis stage.

Check the displayed error message and verify the input path, file contents, and required column names before rerunning the pipeline.

## Limitations

- The main command-line pipeline accepts CSV input.
- JSON loading is available in the data-loading module, but JSON is not currently integrated as an input option in the main command-line workflow.
- The pipeline runs locally and does not use a database, cloud platform, or streaming service.
- The invalid-record rules focus on quantity and unit-price validation; high positive values are not automatically classified as invalid.
- The analysis is intended for learning and demonstration rather than production deployment.

## Learning Outcomes

This project provides practical experience with:

- Modular Python application design.
- Data ingestion and transformation.
- Pandas DataFrame operations.
- Missing-value and duplicate handling.
- Data validation and invalid-record reporting.
- Grouping and aggregation.
- Sales KPI calculation.
- CSV and Parquet conversion.
- Data visualization.
- Command-line arguments and exception handling.
- Testing an end-to-end data processing workflow.

## License

This project is distributed under the license specified in the `LICENSE` file.
