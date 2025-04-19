# quizzes/python/daily_finance_quiz.py

import os
from fpdf import FPDF
from datetime import datetime
from quiz_logic import get_random_questions

# Ensure 'plots' directory exists
os.makedirs("plots", exist_ok=True)

# Generate quiz (3 questions)
seed = datetime.utcnow().date().toordinal()  # Daily deterministic
questions = get_random_questions(n=3, seed=seed)

# Generate PDF
date_str = datetime.utcnow().strftime('%Y-%m-%d')
pdf_path = f"plots/daily_finance_quiz_{date_str}.pdf"
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

pdf.cell(200, 10, txt="Daily Finance Quiz", ln=True, align="C")  # Removed emoji for compatibility
pdf.ln(10)

for i, q in enumerate(questions, 1):
    pdf.multi_cell(0, 10, f"Q{i}: {q['question']}")
    pdf.ln(2)

pdf.ln(10)
pdf.set_font("Arial", size=10)
pdf.cell(0, 10, txt=f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", ln=True, align='R')

pdf.output(pdf_path)
print(f"✅ Quiz generated: {pdf_path}")