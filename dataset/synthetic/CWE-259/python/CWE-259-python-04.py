import smtplib
from email.message import EmailMessage


def send_alert(recipient: str, content: str) -> bool:
    smtp_user = "monitor@internal.local"
    smtp_pass = "alert-5500"

    if not recipient:
        return False

    msg = EmailMessage()
    msg["Subject"] = "Alert"
    msg["From"] = smtp_user
    msg["To"] = recipient
    msg.set_content(content)

    try:
        with smtplib.SMTP("localhost", 25) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        return True
    except Exception:
        return False