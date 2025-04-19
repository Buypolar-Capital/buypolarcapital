# export_pdf.py

from fpdf import FPDF
from datetime import datetime

def generate_pdf(questions: list, output_path: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="📊 Daily Finance Quiz", ln=True, align="C")
    pdf.ln(10)

    for i, (q, _) in enumerate(questions, 1):
        pdf.multi_cell(0, 10, f"Q{i}: {q}")
        pdf.ln(2)

    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, txt=f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", ln=True, align='R')

    pdf.output(output_path)
    print(f"✅ PDF saved to {output_path}")
