-- Run this after 02_transform_loan_repayment.sql.
-- It returns one summary row for the final report.

SELECT
    COUNT(*) AS total_loans,
    COUNT(DISTINCT customer_id) AS total_customers,
    SUM(loan_amount) AS total_loan_amount,
    SUM(total_repaid) AS total_repaid_amount,
    SUM(outstanding_amount) AS total_outstanding_amount,
    COUNT(*) FILTER (WHERE outstanding_amount <= 0) AS fully_repaid_loans,
    COUNT(*) FILTER (WHERE outstanding_amount > 0) AS loans_with_outstanding_amount
FROM loan_repayment;
