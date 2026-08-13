-- This script expects these staging tables to be loaded from the CSV files:
-- staging_customers, staging_loans, and staging_repayments.
-- The staging tables keep the original source columns.

TRUNCATE TABLE loan_repayment;

WITH latest_customers AS (
    -- Keep one customer row when customer_id appears more than once.
    SELECT DISTINCT ON (customer_id)
        customer_id,
        country,
        customer_type
    FROM staging_customers
    WHERE customer_id IS NOT NULL
      AND customer_id <> ''
    ORDER BY customer_id, last_modified_date DESC
),
latest_loans AS (
    -- Keep one loan row when loan_number appears more than once.
    SELECT DISTINCT ON (loan_number)
        loan_number,
        customer_id,
        application_state,
        loan_amount,
        commencement_date,
        due_date
    FROM staging_loans
    WHERE loan_number IS NOT NULL
      AND loan_number <> ''
      AND loan_amount >= 0
    ORDER BY loan_number, last_modified_date DESC
),
valid_repayments AS (
    -- Only use successful repayments with a positive or zero amount.
    SELECT DISTINCT ON (repayment_id)
        repayment_id,
        loan_number,
        amount,
        UPPER(repayment_status) AS repayment_status
    FROM staging_repayments
    WHERE loan_number IS NOT NULL
      AND loan_number <> ''
      AND amount >= 0
      AND UPPER(repayment_status) IN ('PROCESSED', 'SUCCESS', 'COMPLETE')
    ORDER BY repayment_id, last_modified_date DESC
),
repayment_totals AS (
    SELECT
        loan_number,
        SUM(amount) AS total_repaid,
        COUNT(*) AS repayment_count,
        MAX(repayment_status) AS repayment_status
    FROM valid_repayments
    GROUP BY loan_number
)
INSERT INTO loan_repayment (
    loan_number,
    customer_id,
    country,
    customer_type,
    application_state,
    loan_amount,
    commencement_date,
    due_date,
    total_repaid,
    outstanding_amount,
    repayment_count,
    repayment_status
)
SELECT
    loans.loan_number,
    loans.customer_id,
    customers.country,
    customers.customer_type,
    loans.application_state,
    loans.loan_amount,
    loans.commencement_date,
    loans.due_date,
    COALESCE(repayments.total_repaid, 0) AS total_repaid,
    loans.loan_amount - COALESCE(repayments.total_repaid, 0) AS outstanding_amount,
    COALESCE(repayments.repayment_count, 0) AS repayment_count,
    COALESCE(repayments.repayment_status, 'NO_REPAYMENT') AS repayment_status
FROM latest_loans AS loans
INNER JOIN latest_customers AS customers
    ON loans.customer_id = customers.customer_id
LEFT JOIN repayment_totals AS repayments
    ON loans.loan_number = repayments.loan_number;
