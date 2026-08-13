"""Create a basic data quality report from the source CSV files."""

import csv
from collections import Counter
from pathlib import Path


project_folder = Path(__file__).resolve().parents[1]
source_folder = project_folder / "Datasets" / "source"
report_file = project_folder / "reports" / "data_quality_report.md"
csv_files = ["customers.csv", "loans.csv", "repayments.csv"]

report_lines = [
    "# Data Quality Report",
    "",
    "## Stage 1 - Understand the data",
    "",
    "This report was created from the original CSV files in `Datasets/source`.",
    "",
    "## File summary",
    "",
    "| File | Rows | Columns | Duplicate rows |",
    "|---|---:|---:|---:|",
]

all_data = {}

for file_name in csv_files:
    file_path = source_folder / file_name

    with file_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
        columns = reader.fieldnames

    all_data[file_name] = {"rows": rows, "columns": columns}

    row_values = []
    for row in rows:
        row_values.append(tuple(row.values()))

    duplicate_rows = len(row_values) - len(set(row_values))

    report_lines.append(
        f"| {file_name} | {len(rows):,} | {len(columns)} | {duplicate_rows:,} |"
    )

for file_name in csv_files:
    rows = all_data[file_name]["rows"]
    columns = all_data[file_name]["columns"]

    report_lines.extend(
        [
            "",
            f"### {file_name}",
            "",
            "| Column | Missing values |",
            "|---|---:|",
        ]
    )

    for column in columns:
        missing_values = 0

        for row in rows:
            value = row[column]
            if value is None or value.strip().lower() in ["", "nan", "null", "none"]:
                missing_values += 1

        column_name = column if column else "(blank header)"
        report_lines.append(f"| {column_name} | {missing_values:,} |")

report_lines.extend(
    [
        "",
        "## Values to review",
        "",
        "| Field | Different values found |",
        "|---|---|",
    ]
)

fields_to_review = [
    ("customers.csv", "country"),
    ("customers.csv", "customer_type"),
    ("loans.csv", "application_state"),
    ("loans.csv", "is_top_up"),
    ("repayments.csv", "repayment_status"),
]

for file_name, column in fields_to_review:
    values = Counter()

    for row in all_data[file_name]["rows"]:
        value = row[column].strip()
        if value:
            values[value] += 1

    value_text = ", ".join(f"`{value}` ({count:,})" for value, count in sorted(values.items()))
    report_lines.append(f"| {file_name} - {column} | {value_text} |")

report_lines.extend(
    [
        "",
        "## Relationships to validate",
        "",
        "- Each loan customer ID should be found in the customers file.",
        "- Each repayment loan number should be found in the loans file.",
        "",
        "Detailed validation findings are in `reports/data_validation_results.md`.",
    ]
)

report_file.parent.mkdir(exist_ok=True)
report_file.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

print("Data quality report created:", report_file)
