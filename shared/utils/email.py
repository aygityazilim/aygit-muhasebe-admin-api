import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from shared.config import Config

class EmailUtils:
    TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

    @staticmethod
    async def send_email(
            template_name: str,
            subject: str,
            to_email: str, 
            **kwargs
        ):
        template_str = Path(f"{EmailUtils.TEMPLATES_DIR}/{template_name}").read_text(encoding="utf-8")
        template_str = template_str.format(**kwargs)
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = Config.NOREPLY_EMAIL
        msg["To"] = to_email
        
        html = MIMEText(template_str, "html", "utf-8")
        msg.attach(html)

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(Config.NOREPLY_EMAIL, Config.NOREPLY_PASSWORD)
        server.sendmail(Config.NOREPLY_EMAIL, [to_email], msg.as_bytes())
