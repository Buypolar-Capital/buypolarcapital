# quizzes/python/export_html.py

import os
from datetime import datetime

def save_quiz_to_html(questions, output_path="plots/daily_finance_quiz.html", show_answers=False):
    """
    Export quiz to a simple styled HTML file.

    Args:
        questions: list of dicts with 'question' and 'answer' keys
        output_path: where to save the HTML file
        show_answers: whether to include answers
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    html = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "  <meta charset='UTF-8'>",
        "  <title>Daily Finance Quiz</title>",
        "  <style>",
        "    body { font-family: Arial, sans-serif; padding: 2em; max-width: 700px; margin: auto; }",
        "    h1 { text-align: center; }",
        "    .question { margin-bottom: 1em; }",
        "    .answer { color: #555; margin-top: 0.25em; }",
        "    .timestamp { text-align: right; font-size: 0.85em; color: #777; margin-top: 3em; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <h1>Daily Finance Quiz</h1>"
    ]

    for i, q in enumerate(questions, 1):
        html.append(f"<div class='question'><strong>Q{i}.</strong> {q['question']}")
        if show_answers:
            answer = q.get('answer', "No answer provided.")
            html.append(f"<div class='answer'><em>Answer:</em> {answer}</div>")
        html.append("</div>")

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    html.append(f"<div class='timestamp'>Generated: {timestamp}</div>")

    html.append("</body></html>")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html))

    print(f"✅ HTML saved to {output_path}")