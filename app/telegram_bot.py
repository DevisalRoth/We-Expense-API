import os
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def send_telegram_notification(chat_id: str, expense_data: dict, receipt_data: bytes = None):
    if not TELEGRAM_BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN not set")
        return False

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    
    message = (
        f"Dear {expense_data.get('recipient_name', 'User')},\n"
        f"You have a new expense from {expense_data.get('sender_name', 'We Expense App')}.\n\n"
        f"Expense Title: {expense_data['title']}\n"
        f"Total Amount Due: ${expense_data['amount']}\n"
        f"Date: {expense_data['date']}\n\n"
        f"Thank you,\n"
        f"Powered by: https://weexpense.com"
    )

    try:
        if receipt_data:
            # Debugging: Print first 20 bytes to check if it's a valid image header
            print(f"📸 Received receipt_data: {len(receipt_data)} bytes")
            print(f"🔍 Header (Hex): {receipt_data[:20].hex()}")
            
            # Check if it needs explicit Base64 decoding (sometimes Pydantic/FastAPI interactions vary)
            import base64
            # If it doesn't look like a JPEG (FF D8) or PNG (89 50), try decoding
            # Common Headers: JPEG=ffd8..., PNG=89504e47...
            header = receipt_data[:4]
            if header != b'\xff\xd8\xff\xe0' and header != b'\xff\xd8\xff\xe1' and header != b'\x89\x50\x4e\x47':
                try:
                    # Attempt to decode if it looks like base64 chars
                    decoded_data = base64.b64decode(receipt_data)
                    print("⚠️ Data was Base64 encoded. Decoded successfully.")
                    receipt_data = decoded_data
                except Exception:
                    # Not base64 or failed, proceed with original
                    pass

            # Use httpx for direct API call to avoid library issues with file handling
            import httpx
            
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            
            data = {
                "chat_id": chat_id,
                "caption": message
            }
            
            files = {
                "photo": ("receipt.jpg", receipt_data, "image/jpeg")
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=data, files=files)
                if response.status_code != 200:
                    print(f"Telegram API Error: {response.text}")
                    return False
        else:
            await bot.send_message(chat_id=chat_id, text=message)
        return True
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False
