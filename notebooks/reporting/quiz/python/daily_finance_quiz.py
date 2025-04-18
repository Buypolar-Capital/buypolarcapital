# quizzes/python/daily_finance_quiz.py

import random
import os
from fpdf import FPDF
from datetime import datetime

# Ensure 'plots' directory exists
os.makedirs("plots", exist_ok=True)

# Example questions (can be moved to a JSON or external file)
QUESTIONS = [
    ("What is the formula for the Sharpe Ratio?", "Expected return minus risk-free rate divided by standard deviation."),
    ("What does CAPM stand for?", "Capital Asset Pricing Model."),
    ("What is the interpretation of beta in finance?", "A measure of a stock's volatility relative to the market."),
    ("What is convexity in bond pricing?", "A measure of the curvature in the relationship between bond prices and yields."),
    ("Explain the difference between systematic and unsystematic risk.", "Systematic risk affects the entire market, unsystematic is asset-specific.")
]

# Select a random subset
quiz_questions = random.sample(QUESTIONS, 3)

# Generate PDF
pdf_path = "plots/daily_finance_quiz.pdf"
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

pdf.cell(200, 10, txt="📊 Daily Finance Quiz", ln=True, align="C")
pdf.ln(10)

for i, (q, _) in enumerate(quiz_questions, 1):
    pdf.multi_cell(0, 10, f"Q{i}: {q}")
    pdf.ln(2)

pdf.ln(10)
pdf.set_font("Arial", size=10)
pdf.cell(0, 10, txt=f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", ln=True, align='R')

pdf.output(pdf_path)
print(f"✅ Quiz generated: {pdf_path}")
