# Data Quality Report

## Stage 1 - Understand the data

This report was created from the original CSV files in `Datasets/source`.

## File summary

| File | Rows | Columns | Duplicate rows |
|---|---:|---:|---:|
| customers.csv | 18,011 | 11 | 25 |
| loans.csv | 23,575 | 16 | 20 |
| repayments.csv | 18,431 | 11 | 30 |

### customers.csv

| Column | Missing values |
|---|---:|
| customer_id | 0 |
| active | 0 |
| created_at | 0 |
| createdat_id | 0 |
| last_modified_date | 0 |
| last_modified_date_id | 0 |
| country | 0 |
| customer_type | 0 |
| document_number | 35 |
| document_type | 0 |
| customer_role | 0 |

### loans.csv

| Column | Missing values |
|---|---:|
| loan_number | 0 |
| customer_id | 40 |
| created_at | 0 |
| createdat_id | 0 |
| last_modified_date | 0 |
| last_modified_date_id | 0 |
| application_state | 0 |
| credit_limit | 623 |
| disbursable_amount | 623 |
| is_top_up | 0 |
| loan_amount | 30 |
| commencement_date | 25 |
| commencement_date_id | 25 |
| due_date | 2,813 |
| due_date_id | 2,813 |
| request_balance | 2,813 |

### repayments.csv

| Column | Missing values |
|---|---:|
| repayment_id | 0 |
| created_at | 0 |
| createdat_id | 0 |
| last_modified_date | 0 |
| last_modified_date_id | 0 |
| amount | 25 |
| batch_ref | 1,403 |
| loan_number | 15 |
| repayment_status | 0 |
| transaction_narrative | 0 |
| (blank header) | 18,430 |

## Values to review

| Field | Different values found |
|---|---|
| customers.csv - country | `KE` (27), `KENYA` (21), `Kenya` (17,942), `kenya` (21) |
| customers.csv - customer_type | `0` (4), `CORPORATE` (7), `INDIVIDUAL` (17,868), `Individual` (32), `N/A` (8), `iNDIVIDUAL` (38), `individual` (54) |
| loans.csv - application_state | `COMPLETE` (5), `DISBURSEMENT_FAILED` (402), `EXISTING_LOAN` (18), `EXISTING_LOAN_IN_DEFAULT` (195), `EXPIRED` (1,785), `INIT_CHECKS_APPROVED` (4), `LIMIT_EXCEEDED` (33), `PENDING_APPLICATION_FOUND` (352), `PROCESSD` (7), `PROCESSED` (20,742), `Pending` (4), `SUBSCRIPTION_DECLINED` (24), `UNKNOWN` (4) |
| loans.csv - is_top_up | `2` (4), `N/A` (8), `f` (23,555), `maybe` (3), `top-up` (5) |
| repayments.csv - repayment_status | `FAILED` (116), `PROCESSED` (18,295), `Pending` (6), `Reversed` (4), `SUCCESS` (4), `complete` (6) |

## Relationships to validate

- Each loan customer ID should be found in the customers file.
- Each repayment loan number should be found in the loans file.

Detailed validation findings are in `reports/data_validation_results.md`.
