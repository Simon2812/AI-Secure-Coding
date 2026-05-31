import smtplib
from email.mime.text import MIMEText

SMTP_HOST = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "alerts@example.com"
SMTP_PASS = "S3cr3tP@ssw0rd!"

def send_alert(recipient, body):
    msg = MIMEText(body)
    msg["Subject"] = "Alert"
    msg["From"] = SMTP_USER
    msg["To"] = recipient

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASS)
    server.sendmail(SMTP_USER, [recipient], msg.as_string())
    server.quit()
