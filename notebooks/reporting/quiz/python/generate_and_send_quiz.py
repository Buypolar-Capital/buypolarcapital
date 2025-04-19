# quizzes/python/generate_and_send_quiz.py

from quiz_logic import get_random_questions
from export_pdf import generate_pdf
from export_html import save_quiz_to_html
import os
from datetime import datetime

def run_daily_quiz(to_email):
    # Ensure 'plots' directory exists
    os.makedirs("plots", exist_ok=True)

    # Step 1: Get quiz questions
    questions = get_random_questions(n=3)

    # Step 2: Generate outputs
    date_str = os.getenv('LATEST_DATE', datetime.utcnow().strftime('%Y-%m-%d'))
    pdf_path = f"plots/daily_finance_quiz_{date_str}.pdf"
    html_path = f"plots/daily_finance_quiz_{date_str}.html"

    generate_pdf(questions, pdf_path)
    save_quiz_to_html(questions, html_path)

    print(f"✅ Quiz files generated: {pdf_path}, {html_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate a daily finance quiz.")
    parser.add_argument("--email", required=True, help="Recipient email address (not used in script)")
    args = parser.parse_args()

    run_daily_quiz(args.email)