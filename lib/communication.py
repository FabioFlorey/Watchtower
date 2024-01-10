import win32com.client as win32
import yaml
from datetime import datetime

CONFIG_PATH = "./conf/config.yaml"
WEBSITES_PATH = "./conf/websites.yaml"
TEMPLATE_PATH = "./template/email.html"

def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return ""

def read_config(file_path):
    config_content = read_file(file_path)
    return yaml.safe_load(config_content)

def generate_error_table(data):
    html_table = []

    for website, details in data.items():
        website_name = website
        website_url = details.get('url')

        if details.get('status_code', [])[0] != 200:
            html_table.append(f"<tr><td>{website_name}</td><td>{website_url}</td><td>Errore nello status code {details.get('status_code')}</td></tr>")

        if not details.get('html_checksum'):
            html_table.append(f"<tr><td>{website_name}</td><td>{website_url}</td><td>Cambiamenti HTML, errore nel checksum HTML</td></tr>")

        if not details.get('image_checksum'):
            html_table.append(f"<tr><td>{website_name}</td><td>{website_url}</td><td>Grafica cambiata, errore nel checksum tra screenshot</td></tr>")

    if not html_table:
        return ""  # Return an empty string if there are no errors

    html_email_table = f"""
    <table>
      <tr>
        <th>Nome</th>
        <th>URL</th>
        <th>Anomalia</th>
      </tr>
      {''.join(html_table)}
    </table>
    """
    return html_email_table


def send_outlook_email(recipient, subject, body):
    try:
        outlook = win32.Dispatch('Outlook.Application')
        mail = outlook.CreateItem(0)
        mail.To = recipient
        mail.Subject = subject
        mail.HTMLBody = body
        mail.Send()
    except Exception as e:
        print(f"Error sending email: {e}")

def send_mail():
    try:
        config = read_config(CONFIG_PATH)

        email_config = config.get("COMMUNICATION", {}).get("EMAIL", {})
        recipient_email = email_config.get("recipient", "")
        email_subject = email_config.get("subject", "Watchtower (Automated Email)")

        websites_data = read_config(WEBSITES_PATH)
        html_table = generate_error_table(websites_data)
    
        email_body_template = read_file(TEMPLATE_PATH)

        email_body = email_body_template.replace("[TABLES]", html_table)
        email_body = email_body.replace('[TODAY]', datetime.strftime(datetime.now(), 'alle %H:%M del %d/%m/%Y'))

        if html_table:
            send_outlook_email(recipient_email, email_subject, email_body)
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    send_mail()
