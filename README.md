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

This creates the project virtual environment in `.venv` and installs the Python dependencies.

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

## Pipeline execution order

Run the project in this order:

1. Run `notebooks/data_inspection.ipynb` to inspect the original files.
2. Run `uv run python scripts/profile_data.py`.
3. Run `uv run python scripts/validate_data.py`.
4. Review the two Markdown reports in `reports/`.
5. Load the CSV files into PostgreSQL staging tables.
6. Run the SQL scripts in the order shown below.

## Assumptions

- `customer_id`, `loan_number`, and `repayment_id` are the identifiers for customers, loans, and repayments.
- A loan belongs to one customer through `customer_id`.
- A repayment belongs to one loan through `loan_number`.
- A positive repayment is included in the total only when its status is `PROCESSED`, `SUCCESS`, or `COMPLETE`.
- When an identifier has duplicate records, the latest `last_modified_date` record is used in the SQL transformation.
- Negative loan amounts and negative repayment amounts are treated as invalid and are excluded from the final table.

## Data quality findings and handling

The profiling and validation scripts identified the following source-data issues:

| Issue found | Handling in this project |
|---|---|
| Duplicate customer IDs, loan numbers, and repayment IDs | The SQL transformation keeps the latest record by `last_modified_date`. |
| Repayments with no matching loan | They do not join to a loan, so they are excluded from the final `loan_repayment` table. |
| Values other than `t` and `f` in `is_top_up` | These are reported by validation. The field is not used in the final table. |
| Negative loan and repayment amounts | They are reported by validation and excluded by the SQL transformation. |
| Invalid repayment dates | They are reported by validation. Dates are not used to calculate the current summary. |
| Different casing and spelling in categorical values | Values are preserved except repayment status, which is converted to uppercase for the repayment calculation. |

The original CSV files are never changed. The reports provide the evidence for the quality checks:

- `reports/data_quality_report.md`
- `reports/data_validation_results.md`

## PostgreSQL

The final PostgreSQL table is named `loan_repayment`.

Before running the transformation, load the CSV files into these staging tables:

- `staging_customers`
- `staging_loans`
- `staging_repayments`

The staging tables should use the same column names as their source CSV files. They are used to keep the original imported data separate from the cleaned final table.

### Create and configure the database

PostgreSQL must be installed locally and the `psql` command must be available. The following example creates a database and a user. Change the password before using it.

```sql
CREATE ROLE loan_repayment_user WITH LOGIN PASSWORD 'your_password';
CREATE DATABASE loan_repayment_db OWNER loan_repayment_user;
```

Connect to the new database:

```powershell
psql -h localhost -p 5432 -U loan_repayment_user -d loan_repayment_db
```

The transformation expects `staging_customers`, `staging_loans`, and `staging_repayments` to already contain the corresponding CSV data. Their columns must have the same names as the source files.

Run the SQL scripts in this order:

1. `sql/01_create_loan_repayment_table.sql`
2. `sql/02_transform_loan_repayment.sql`
3. `sql/03_summary_report.sql`
4. `sql/04_test_loan_repayment.sql`

The transformation removes duplicate IDs by keeping the latest record, excludes negative loan and repayment amounts, and only includes repayments marked `PROCESSED`, `SUCCESS`, or `COMPLETE` in repayment totals.

`04_test_loan_repayment.sql` is a simple post-transformation test. Each `issue_count` should be zero.

## Database design

The final table, `loan_repayment`, has one row per cleaned loan. It contains:

- loan and customer identifiers
- customer country and customer type
- loan application state, amount, commencement date, and due date
- total repayment amount and repayment count
- outstanding amount, calculated as loan amount minus total repaid
- final repayment status

The staging tables keep imported source values separate from the final table. This makes it possible to rerun the transformation without modifying the original files.

## Limitations

- PostgreSQL staging-table creation and CSV loading are not automated in this repository.
- The SQL scripts have been written and reviewed but have not been run against a local PostgreSQL database in this project environment.
- The summary report is a SQL query. It will return values after the staging tables are loaded and the transformation is run.
- The current transformation excludes invalid records instead of creating a separate rejected-records table.
