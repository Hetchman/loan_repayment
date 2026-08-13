# Loan Repayment Data Pipeline

This project is a junior data engineering practical assessment. It works with customer, loan, and repayment CSV files and prepares the data for loading into PostgreSQL.

## Project approach

1. Inspect the source data in a Jupyter notebook.
2. Create repeatable Python scripts for profiling and validation.
3. Review data-quality issues before loading data.
4. Load validated data into PostgreSQL staging tables.
5. Transform the staging data with SQL.

The original CSV files are kept unchanged in `Datasets/source`.

## Project structure

```text
Datasets/source/             Original CSV files and data dictionary
notebooks/data_inspection.ipynb
scripts/profile_data.py      Creates the data quality report
scripts/validate_data.py     Runs data validation checks
reports/                     Generated reports
sql/                         PostgreSQL transformation, report, and test scripts
```

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for the virtual environment and dependencies.

```powershell
uv sync
```

To use the notebook, start Jupyter from the project folder:

```powershell
uv run jupyter lab
```

Open `notebooks/data_inspection.ipynb` and run its cells from top to bottom.

## Run the data checks

From the project folder, run:

```powershell
uv run python scripts/profile_data.py
uv run python scripts/validate_data.py
```

The scripts create:

- `reports/data_quality_report.md`
- `reports/data_validation_results.md`

The validation script reports source-data issues for review. It does not change the original files.

## PostgreSQL

The final PostgreSQL table is named `loan_repayment`.

Before running the transformation, load the CSV files into these staging tables:

- `staging_customers`
- `staging_loans`
- `staging_repayments`

The staging tables should use the same column names as their source CSV files. They are used to keep the original imported data separate from the cleaned final table.

Run the SQL scripts in this order:

1. `sql/01_create_loan_repayment_table.sql`
2. `sql/02_transform_loan_repayment.sql`
3. `sql/03_summary_report.sql`
4. `sql/04_test_loan_repayment.sql`

The transformation removes duplicate IDs by keeping the latest record, excludes negative loan and repayment amounts, and only includes repayments marked `PROCESSED`, `SUCCESS`, or `COMPLETE` in repayment totals.

`04_test_loan_repayment.sql` is a simple post-transformation test. Each `issue_count` should be zero.
