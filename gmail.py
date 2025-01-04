import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import ast
import yaml

load_dotenv()  # Charger les variables d'environnement

subject = "Maisons à vendre 2"
body = "This is the body of the text message"
sender =  os.getenv('EMAIL_SENDER')
recipients = ast.literal_eval(os.getenv('EMAIL_RECIPIENTS')) # 
password = os.getenv('EMAIL_PASSWORD')

# Charger le fichier maisons.yaml en un dictionnaire Python
with open('maisons.yaml', 'r', encoding='utf-8') as file:
    maisons_data = yaml.safe_load(file) 

# Convertir le contenu YAML en texte brut
yaml_content = yaml.dump(maisons_data, allow_unicode=True, sort_keys=False)


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")


send_email(subject, yaml_content, sender, recipients, password)