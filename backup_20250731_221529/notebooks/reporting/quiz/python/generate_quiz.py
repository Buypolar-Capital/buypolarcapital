# notebooks/reporting/quiz/python/generate_quiz.py

from quiz_logic import get_random_questions
from export_pdf import generate_pdf
from export_html import save_quiz_to_html
from export_markdown import save_quiz_to_markdown
from send_email import send_quiz_email
import os
from datetime import datetime
import argparse

def generate_daily_quiz(to_email=None):
    # Ensure 'plots' directory exists
    os.makedirs("plots", exist_ok=True)

    # Step 1: Get quiz questions
    questions = get_random_questions(n=3)

    # Step 2: Generate outputs
    date_str = datetime.utcnow().strftime('%Y-%m-%d')
    pdf_path = f"plots/daily_finance_quiz_{date_str}.pdf"
    html_path = f"plots/daily_finance_quiz_{date_str}.html"
    md_path = f"plots/daily_finance_quiz_{date_str}.md"

    generate_pdf(questions, pdf_path)
    save_quiz_to_html(questions, html_path)
    save_quiz_to_markdown(questions, md_path)

    print(f"✅ Quiz files generated:")
    print(f"  - PDF: {pdf_path}")
    print(f"  - HTML: {html_path}")
    print(f"  - Markdown: {md_path}")

    # Step 3: Send email if to_email is provided
    if to_email:
        subject = f"Daily Finance Quiz – {date_str}"
        body = "Hi there!\n\nAttached you'll find today's finance quiz in PDF, HTML, and Markdown formats. Have fun!\n\n– BuyPolar Capital"
        
        send_quiz_email(
            subject=subject,
            to_email=to_email,
            body_text=body,
            attachments=[pdf_path, html_path, md_path]
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a daily finance quiz and optionally send it via email.")
    parser.add_argument("--email", help="Recipient email address")
    args = parser.parse_args()

    generate_daily_quiz(to_email=args.email)