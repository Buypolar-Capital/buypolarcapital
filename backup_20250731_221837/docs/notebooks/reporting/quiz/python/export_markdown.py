# quizzes/python/export_markdown.py

import os
from datetime import datetime

def save_quiz_to_markdown(questions, output_path="plots/daily_finance_quiz.md", show_answers=False):
    """
    Save a quiz to a markdown (.md) file.

    Args:
        questions: list of dicts with 'question' and 'answer' keys
        output_path: file path to save the markdown
        show_answers: whether to include answers
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Daily Finance Quiz\n\n")

        for i, q in enumerate(questions, 1):
            f.write(f"**Q{i}.** {q['question']}\n\n")
            if show_answers:
                answer = q.get('answer', "No answer provided.")
                f.write(f"> **Answer:** {answer}\n\n")

        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        f.write(f"\n---\n\n_Generated on {timestamp}_\n")

    print(f"✅ Markdown saved to {output_path}")