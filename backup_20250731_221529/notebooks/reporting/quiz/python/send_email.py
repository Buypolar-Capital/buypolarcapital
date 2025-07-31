# notebooks/reporting/quiz/python/send_email.py

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_quiz_email(
    subject,
    to_email,
    body_text,
    attachments=None,
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    from_email=None,
    from_password=None,
):
    """
    Send an email with optional PDF/HTML/Markdown attachments.

    Args:
        subject: Email subject line
        to_email: Recipient email address
        body_text: Email body in plain text
        attachments: List of file paths to attach (e.g., PDF/HTML/MD)
        smtp_server: SMTP server address
        smtp_port: SMTP port (default Gmail TLS)
        from_email: Sender email (or set via ENV VARS)
        from_password: Password or app token (or set via ENV VARS)
    """
    from_email = from_email or os.getenv("BPC_EMAIL")
    from_password = from_password or os.getenv("BPC_EMAIL_PASSWORD")

    if not from_email or not from_password:
        raise ValueError("Missing email credentials (set BPC_EMAIL and BPC_EMAIL_PASSWORD env vars).")

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body_text, "plain"))

    # Attach files
    for path in attachments or []:
        with open(path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(path))
        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(path)}"'
        msg.attach(part)

    # Send
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)

    print(f"📧 Email sent to {to_email}")