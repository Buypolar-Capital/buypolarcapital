# init_questions_db.py

import duckdb
import os

# Ensure the data folder exists
os.makedirs("quiz_data", exist_ok=True)

# Connect to DuckDB file
con = duckdb.connect("quiz_data/questions.duckdb")

# Create table
con.execute("""
CREATE TABLE IF NOT EXISTS quiz_questions (
    id INTEGER PRIMARY KEY,
    question TEXT,
    answer TEXT
)
""")

# Insert sample questions
sample_data = [
    (1, "What is the formula for the Sharpe Ratio?", "Expected return minus risk-free rate divided by standard deviation."),
    (2, "What does CAPM stand for?", "Capital Asset Pricing Model."),
    (3, "What is the interpretation of beta in finance?", "A measure of a stock's volatility relative to the market."),
    (4, "What is convexity in bond pricing?", "A measure of the curvature in the relationship between bond prices and yields."),
    (5, "Explain the difference between systematic and unsystematic risk.", "Systematic risk affects the entire market, unsystematic is asset-specific.")
]

# Insert data if table is empty
existing_rows = con.execute("SELECT COUNT(*) FROM quiz_questions").fetchone()[0]
if existing_rows == 0:
    con.executemany("INSERT INTO quiz_questions VALUES (?, ?, ?)", sample_data)
    print("✅ Sample questions inserted.")
else:
    print("ℹ️ Questions already exist.")

con.close()
