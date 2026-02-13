import os
import asyncio
import httpx
from dotenv import load_dotenv

# Force reload of .env
load_dotenv(override=True)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = "784259869"

print(f"--- Telegram Real Image Test ---")

async def test_real_photo():
    if not TELEGRAM_BOT_TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN is missing!")
        return

    print("\n1. Downloading a valid sample image...")
    image_url = "https://picsum.photos/200/300" # Random valid image
    
    async with httpx.AsyncClient() as client:
        try:
            img_response = await client.get(image_url, follow_redirects=True)
            if img_response.status_code != 200:
                print("❌ Failed to download sample image.")
                return
            image_data = img_response.content
            print(f"✅ Downloaded {len(image_data)} bytes.")
        except Exception as e:
            print(f"❌ Error downloading image: {e}")
            return

    print("\n2. Sending valid image to Telegram...")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    
    data = {
        "chat_id": CHAT_ID,
        "caption": "📸 Real Image Test: If you see this, image sending works!"
    }
    
    files = {
        "photo": ("test_image.jpg", image_data, "image/jpeg")
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data, files=files)
            
            if response.status_code == 200:
                print("✅ SUCCESS! Real photo sent successfully.")
            else:
                print(f"❌ FAILED! Status: {response.status_code}")
                print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ FAILED! Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_real_photo())
