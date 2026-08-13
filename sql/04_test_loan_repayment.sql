-- Simple checks for the final table.
-- Every issue_count should be 0 after the transformation.

SELECT 'duplicate loan numbers' AS test_name, COUNT(*) AS issue_count
FROM (
    SELECT loan_number
    FROM loan_repayment
    GROUP BY loan_number
    HAVING COUNT(*) > 1
) AS duplicate_loans

UNION ALL

SELECT 'negative loan amounts', COUNT(*)
FROM loan_repayment
WHERE loan_amount < 0

UNION ALL

SELECT 'negative total repaid amounts', COUNT(*)
FROM loan_repayment
WHERE total_repaid < 0

UNION ALL

SELECT 'negative repayment counts', COUNT(*)
FROM loan_repayment
WHERE repayment_count < 0

UNION ALL

SELECT 'missing customer IDs', COUNT(*)
FROM loan_repayment
WHERE customer_id IS NULL OR customer_id = '';
