import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = str(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

if not all([EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS]):
    raise ValueError("Variáveis de ambiente não configuradas. Verifique o arquivo .env")

EMAIL_HOST = str(EMAIL_HOST)
EMAIL_PASS = str(EMAIL_PASS)
def send_email_with_pdf(to_email: str, pdf_path: str, subject="Documento Jurídico", body="Segue o documento em anexo."):
    try:
        # Monta a mensagem
        msg = MIMEMultipart()
        msg["From"] = str(EMAIL_USER)
        msg["To"] = to_email
        msg["Subject"] = subject

        # Corpo do email
        msg.attach(MIMEText(body, "plain"))

        # Anexo PDF
        with open(pdf_path, "rb") as f:
            pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
            pdf_attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(pdf_path))
            msg.attach(pdf_attachment)


        with smtplib.SMTP(str(EMAIL_HOST), int(EMAIL_PORT)) as server:
            server.starttls()
            server.login(str(EMAIL_USER), str(EMAIL_PASS))
            server.sendmail(str(EMAIL_USER), to_email, msg.as_string())

        return True, "Email enviado com sucesso."

    except Exception as e:
        return False, f"Erro ao enviar email: {str(e)}"
