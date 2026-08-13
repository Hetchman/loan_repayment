-- This is the final table used for the loan repayment report.

DROP TABLE IF EXISTS loan_repayment;

CREATE TABLE loan_repayment (
    loan_number VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    country VARCHAR(50),
    customer_type VARCHAR(50),
    application_state VARCHAR(50),
    loan_amount NUMERIC(14, 2) NOT NULL,
    commencement_date DATE,
    due_date DATE,
    total_repaid NUMERIC(14, 2) NOT NULL DEFAULT 0,
    outstanding_amount NUMERIC(14, 2) NOT NULL,
    repayment_count INTEGER NOT NULL DEFAULT 0,
    repayment_status VARCHAR(30)
);
