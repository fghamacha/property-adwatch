from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def create_email(subject, body, sender, recipients):
    """Create an email with the given subject and body."""
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg.attach(MIMEText(body, 'html'))
    return msg

def send_email(msg, sender, password):
    """Send an email using SMTP."""
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, msg['To'].split(","), msg.as_string())
