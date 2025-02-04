import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import ast
import yaml
from datetime import datetime

# Get current date and time
now = datetime.now()

# Convert datetime to string using strftime
date_str = now.strftime('%d-%m-%Y  %H:%M')
formatted_date = f"########## {date_str} ##########"

load_dotenv()  # Charger les variables d'environnement

# subject = "Maisons à vendre "+date_str
body = "This is the body of the text message"
sender =  os.getenv('EMAIL_SENDER')
recipients = ast.literal_eval(os.getenv('EMAIL_RECIPIENTS')) # 
password = os.getenv('EMAIL_PASSWORD')

# Obtenir les thread_id depuis les variables d'environnement
thread_id_maisons = os.getenv('EMAIL_THREAD_ID_MAISONS')
thread_id_appartements = os.getenv('EMAIL_THREAD_ID_APPARTEMENTS')

# Charger le fichier maisons.yaml en un dictionnaire Python
with open('maisons.yaml', 'r', encoding='utf-8') as file:
    maisons_data = yaml.safe_load(file) 
with open('appartements.yaml', 'r', encoding='utf-8') as file:
    appartements_data = yaml.safe_load(file)

# Convertir le contenu YAML en texte brut
yaml_content_maisons = yaml.dump(maisons_data, allow_unicode=True, sort_keys=False)
yaml_content_appartements = yaml.dump(appartements_data, allow_unicode=True, sort_keys=False)

# Create new variable containing date and yaml content
email_content_maisons= f"{formatted_date}\n\n{yaml_content_maisons}"
email_content_appartement= f"{formatted_date}\n\n{yaml_content_appartements}"


def send_email(subject, body, sender, recipients, password, thread_id_env_var):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    # Récupérer le Thread-ID depuis l'environnement (si dispo)
    thread_id = os.getenv(thread_id_env_var)
    if thread_id:
        msg['In-Reply-To'] = thread_id
        msg['References'] = thread_id
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message ",subject," sent!")


send_email('Appartement à vendre', email_content_appartement, sender, recipients, password, "EMAIL_THREAD_ID_APPARTEMENTS")
send_email('Maisons à vendre', email_content_maisons, sender, recipients, password, "EMAIL_THREAD_ID_MAISONS")
