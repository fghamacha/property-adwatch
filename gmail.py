from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import ast
import yaml
from datetime import datetime
from jinja2 import Environment, FileSystemLoader


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

# 📂 Fonction pour charger un fichier YAML avec gestion des erreurs
def load_yaml(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            return data if isinstance(data, dict) else {}  # Toujours retourner un dict
    except Exception as e:
        print(f"⚠️ Erreur lors du chargement de {filename}: {e}")
        return {}

# Charger le fichier maisons.yaml en un dictionnaire Python
maisons_data = load_yaml('maisons.yaml')
appartements_data = load_yaml('appartements.yaml')

# 📌 Initialiser Jinja2 pour charger le template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('email.html.j2')

# Générer le contenu HTML
email_body_maisons = template.render(date=date_str, annonces=maisons_data)
email_body_appartements = template.render(date=date_str, annonces=appartements_data)

def send_email(subject, body, sender, recipients, password, thread_id_env_var):
    
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    # Récupérer le Thread-ID depuis l'environnement (si dispo)
    thread_id = os.getenv(thread_id_env_var)
    if thread_id:
        msg['In-Reply-To'] = thread_id
        msg['References'] = thread_id
    
    # Attacher le HTML
    msg.attach(MIMEText(body, 'html')) 

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        print(f"Email envoyé : {subject}")
    except Exception as e:
        print(f"Erreur d'envoi d'email : {e}")


send_email('Appartement à vendre', email_body_appartements, sender, recipients, password, "EMAIL_THREAD_ID_APPARTEMENTS")
send_email('Maisons à vendre', email_body_maisons, sender, recipients, password, "EMAIL_THREAD_ID_MAISONS")
