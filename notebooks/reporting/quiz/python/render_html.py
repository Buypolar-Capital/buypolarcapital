# render_html.py

from datetime import datetime

def generate_html(questions: list, output_path: str):
    date_str = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>📊 Daily Finance Quiz</title>
</head>
<body>
    <h2>📊 Daily Finance Quiz</h2>
    <p><em>Generated: {date_str}</em></p>
    <ol>
"""

    for question, _ in questions:
        html_content += f"<li>{question}</li>\n"

    html_content += """
    </ol>
    <p>— BuyPolar Capital</p>
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ HTML saved to {output_path}")
