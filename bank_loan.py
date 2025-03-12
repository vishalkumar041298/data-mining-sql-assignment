import sqlite3
import random
import faker
from datetime import datetime, timedelta

# Initialize Faker for realistic data generation
fake = faker.Faker()

# Connect to SQLite database
conn = sqlite3.connect("bank_loans.db")
cursor = conn.cursor()

# Create Borrowers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Borrowers (
    borrower_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    credit_score INTEGER CHECK(credit_score BETWEEN 300 AND 850),
    date_of_birth DATE,
    annual_income REAL CHECK(annual_income >= 0),
    risk_category TEXT CHECK(risk_category IN ('Low', 'Medium', 'High'))
);
''')

# Create Loans table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    borrower_id INTEGER,
    loan_type TEXT CHECK(loan_type IN ('Personal', 'Mortgage', 'Auto', 'Business')),
    loan_amount REAL CHECK(loan_amount > 0),
    interest_rate REAL CHECK(interest_rate > 0),
    term_months INTEGER CHECK(term_months > 0),
    FOREIGN KEY (borrower_id) REFERENCES Borrowers(borrower_id)
);
''')

# Create Repayments table (with Foreign and Composite Keys)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Repayments (
    repayment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id INTEGER,
    payment_date DATE,
    amount_paid REAL CHECK(amount_paid >= 0),
    remaining_balance REAL CHECK(remaining_balance >= 0),
    FOREIGN KEY (loan_id) REFERENCES Loans(loan_id)
);
''')

# Populate Borrowers Table with 1,000+ records
risk_levels = ['Low', 'Medium', 'High']
borrowers = []
for _ in range(1000):
    name = fake.name()
    credit_score = random.randint(300, 850)
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%Y-%m-%d')
    annual_income = round(random.uniform(20000, 150000), 2)
    risk_category = 'Low' if credit_score > 700 else 'Medium' if credit_score > 500 else 'High'
    borrowers.append((name, credit_score, date_of_birth, annual_income, risk_category))

cursor.executemany("INSERT INTO Borrowers (name, credit_score, date_of_birth, annual_income, risk_category) VALUES (?, ?, ?, ?, ?)", borrowers)

# Populate Loans Table
loan_types = ['Personal', 'Mortgage', 'Auto', 'Business']
borrower_ids = [row[0] for row in cursor.execute("SELECT borrower_id FROM Borrowers").fetchall()]
loans = []
for _ in range(500):  # Not every borrower will have a loan
    borrower_id = random.choice(borrower_ids)
    loan_type = random.choice(loan_types)
    loan_amount = round(random.uniform(5000, 500000), 2)
    interest_rate = round(random.uniform(2.0, 10.0), 2)
    term_months = random.choice([12, 24, 36, 48, 60, 120, 240])
    loans.append((borrower_id, loan_type, loan_amount, interest_rate, term_months))

cursor.executemany("INSERT INTO Loans (borrower_id, loan_type, loan_amount, interest_rate, term_months) VALUES (?, ?, ?, ?, ?)", loans)

# Populate Repayments Table with 5,000+ transactions
loan_ids = [row[0] for row in cursor.execute("SELECT loan_id FROM Loans").fetchall()]
repayments = []
for _ in range(5000):
    loan_id = random.choice(loan_ids)
    payment_date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
    amount_paid = round(random.uniform(100, 5000), 2)
    remaining_balance = round(random.uniform(0, 500000), 2)
    repayments.append((loan_id, payment_date, amount_paid, remaining_balance))

cursor.executemany("INSERT INTO Repayments (loan_id, payment_date, amount_paid, remaining_balance) VALUES (?, ?, ?, ?)", repayments)

# Commit and close connection
conn.commit()
conn.close()
print("Bank Loan & Credit Risk Database created and populated successfully.")
