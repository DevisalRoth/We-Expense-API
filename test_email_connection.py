import os
import asyncio
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Force reload of .env
load_dotenv(override=True)

print("--- Email Config Test ---")
username = os.getenv("MAIL_USERNAME")
password = os.getenv("MAIL_PASSWORD")
print(f"Username: {username}")
print(f"Password: {password[:2]}...{password[-2:] if password else ''} (Length: {len(password) if password else 0})")

class EmailSettings(BaseSettings):
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
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
    VALIDATE_CERTS=settings.VALIDATE_CERTS
)

async def test_email():
    print("\nAttempting to connect to SMTP server...")
    message = MessageSchema(
        subject="Test Email from FastAPI",
        recipients=[settings.MAIL_USERNAME], # Send to yourself
        body="This is a test email to verify credentials.",
        subtype=MessageType.plain
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        print("✅ SUCCESS! Email sent successfully.")
    except Exception as e:
        print(f"❌ FAILED! Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_email())
