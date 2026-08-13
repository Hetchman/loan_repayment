"""Check important data quality rules before loading the CSV files to PostgreSQL."""

import csv
from collections import Counter
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


project_folder = Path(__file__).resolve().parents[1]
source_folder = project_folder / "Datasets" / "source"
results_file = project_folder / "reports" / "data_validation_results.md"
issues = []

with (source_folder / "customers.csv").open("r", encoding="utf-8-sig", newline="") as csv_file:
    customers = list(csv.DictReader(csv_file))

with (source_folder / "loans.csv").open("r", encoding="utf-8-sig", newline="") as csv_file:
    loans = list(csv.DictReader(csv_file))

with (source_folder / "repayments.csv").open("r", encoding="utf-8-sig", newline="") as csv_file:
    repayments = list(csv.DictReader(csv_file))

# Check that the IDs we expect to use as table keys are not repeated.
for rows, column, file_name in [
    (customers, "customer_id", "customers"),
    (loans, "loan_number", "loans"),
    (repayments, "repayment_id", "repayments"),
]:
    values = []
    missing_values = 0

    for row in rows:
        value = row[column].strip()
        if value:
            values.append(value)
        else:
            missing_values += 1

    duplicate_values = sum(count - 1 for count in Counter(values).values() if count > 1)

    if missing_values > 0:
        issues.append(f"{file_name}: {missing_values:,} missing {column} values")
    if duplicate_values > 0:
        issues.append(f"{file_name}: {duplicate_values:,} duplicate {column} values")

# Check the relationships between the three files.
customer_ids = {row["customer_id"].strip() for row in customers}
loan_numbers = {row["loan_number"].strip() for row in loans}

loans_without_customers = 0
for row in loans:
    customer_id = row["customer_id"].strip()
    if customer_id and customer_id not in customer_ids:
        loans_without_customers += 1

repayments_without_loans = 0
for row in repayments:
    loan_number = row["loan_number"].strip()
    if loan_number and loan_number not in loan_numbers:
        repayments_without_loans += 1

if loans_without_customers > 0:
    issues.append(f"loans.customer_id: {loans_without_customers:,} values have no matching customer")
if repayments_without_loans > 0:
    issues.append(f"repayments.loan_number: {repayments_without_loans:,} values have no matching loan")

# Check simple true/false fields discovered during profiling.
invalid_top_up_values = 0
for row in loans:
    if row["is_top_up"].strip().lower() not in ["t", "f"]:
        invalid_top_up_values += 1

if invalid_top_up_values > 0:
    issues.append(f"loans.is_top_up: {invalid_top_up_values:,} values are not t or f")

# Check that monetary values can be read and are not negative.
for rows, column, file_name in [
    (loans, "loan_amount", "loans"),
    (repayments, "amount", "repayments"),
]:
    invalid_numbers = 0
    negative_numbers = 0

    for row in rows:
        value = row[column].strip()

        if value.lower() in ["", "nan", "null", "none"]:
            continue

        try:
            amount = Decimal(value)
            if amount < 0:
                negative_numbers += 1
        except InvalidOperation:
            invalid_numbers += 1

    if invalid_numbers > 0:
        issues.append(f"{file_name}.{column}: {invalid_numbers:,} values are not valid numbers")
    if negative_numbers > 0:
        issues.append(f"{file_name}.{column}: {negative_numbers:,} values are negative")

# Compare a date field with its YYYYMMDD helper field.
date_problems = 0
for row in repayments:
    try:
        datetime.fromisoformat(row["created_at"].strip())
    except ValueError:
        date_problems += 1

if date_problems > 0:
    issues.append(f"repayments.created_at: {date_problems:,} values are not valid dates")

report_lines = [
    "# Data Validation Results",
    "",
    "Run with `uv run python scripts/validate_data.py`.",
    "",
]

if issues:
    report_lines.extend(["## Issues found", ""])
    for issue in issues:
        report_lines.append(f"- {issue}")
    report_lines.extend(
        [
            "",
            "The source CSV files have not been changed. These issues will be handled in the cleaning and SQL transformation steps.",
        ]
    )
else:
    report_lines.extend(["## Result", "", "All validation checks passed."])

results_file.parent.mkdir(exist_ok=True)
results_file.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

if issues:
    print("Validation completed. Issues found:")
    for issue in issues:
        print("-", issue)
else:
    print("Validation passed.")

print("Validation report created:", results_file)
