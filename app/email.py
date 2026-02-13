import os
from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class EmailSettings(BaseSettings):
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "your_email@gmail.com")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "your_app_password")
    MAIL_FROM: str = os.getenv("MAIL_FROM", "your_email@gmail.com")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", 465))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS", "False").lower() == "true"
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS", "True").lower() == "true"
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

settings = EmailSettings()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
    TEMPLATE_FOLDER=Path(__file__).parent / "templates"
)

async def send_receipt_email(email_to: str, expense_data: dict, receipt_data: bytes = None):
    attachments = []
    
    if receipt_data:
        # Create a temporary file for the attachment
        # FastAPI-Mail typically expects file paths or UploadFile objects,
        # but we can try passing the bytes directly if supported, or save to temp.
        # Let's verify the library version capabilities.
        # Actually, MessageSchema accepts 'attachments' as a list of file paths or UploadFiles.
        # For raw bytes, it's safer to save to a temp file first.
        import tempfile
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(receipt_data)
            tmp.flush()
            attachments.append(tmp.name)
            
    message = MessageSchema(
        subject=f"Receipt for {expense_data['title']}",
        recipients=[email_to],
        template_body=expense_data,
        subtype=MessageType.html,
        attachments=attachments
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message, template_name="receipt.html")
        
        # Clean up temp files
        for file_path in attachments:
            try:
                os.remove(file_path)
            except:
                pass
                
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
