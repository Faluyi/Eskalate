import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

from eskalate.services.email.templates import render_email_template


load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

class EmailService:
    def send_email(self, to_email: str, subject: str, body: str, html: bool = True) -> bool:
        try:
            msg = MIMEMultipart()
            msg["From"] = SMTP_USER
            msg["To"] = to_email
            msg["Subject"] = subject

            if html:
                msg.attach(MIMEText(body, "html"))
            else:
                msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)

            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_verification_email(self, to_email: str, name: str, verification_link: str):
        html_content = render_email_template(
            "verify_email.html",
            subject="Verify Your Email",
            title="Welcome to Job Portal",
            name=name,
            verification_link=verification_link
        )
        return self.send_email(to_email, "Verify Your Email", html_content, html=True)


email_service = EmailService()