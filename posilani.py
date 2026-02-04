import smtplib
from email.mime.text import MIMEText

def send_email_reminder(to_email: str, subject: str, body: str, from_email: str, password: str):
    """Posílá emailovou připomínku."""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.seznam.cz', 465) as server:
        server.login(from_email, password)
        server.send_message(msg)
    print(f"Email odeslán na {to_email}")