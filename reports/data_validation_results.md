# Data Validation Results

Run with `uv run python scripts/validate_data.py`.

## Issues found

- customers: 40 duplicate customer_id values
- loans: 35 duplicate loan_number values
- repayments: 45 duplicate repayment_id values
- repayments.loan_number: 46 values have no matching loan
- loans.is_top_up: 20 values are not t or f
- loans.loan_amount: 15 values are negative
- repayments.amount: 15 values are negative
- repayments.created_at: 15 values are not valid dates

The source CSV files have not been changed. These issues will be handled in the cleaning and SQL transformation steps.
