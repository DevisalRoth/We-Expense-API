import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

# Force reload of .env to get the latest token
load_dotenv(override=True)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# Using the Chat ID you provided
CHAT_ID = "784259869"

print(f"--- Telegram Config Test ---")
print(f"Token: {TELEGRAM_BOT_TOKEN[:5]}...{TELEGRAM_BOT_TOKEN[-5:] if TELEGRAM_BOT_TOKEN else ''}")
print(f"Chat ID: {CHAT_ID}")

async def test_telegram():
    if not TELEGRAM_BOT_TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN is missing!")
        return

    print("\nAttempting to send message to Telegram...")
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    
    try:
        # Get bot info to verify token is valid
        me = await bot.get_me()
        print(f"✅ Bot Connected: @{me.username} ({me.first_name})")
        
        # Send message
        await bot.send_message(chat_id=CHAT_ID, text="🚀 This is a test message from your Expense App!")
        print("✅ SUCCESS! Message sent.")
    except Exception as e:
        print(f"❌ FAILED! Error: {e}")
        print("\nPossible reasons:")
        print("1. You haven't started the bot. Search for your bot username and click START.")
        print("2. The Chat ID is wrong.")
        print("3. The Bot Token is invalid.")

if __name__ == "__main__":
    asyncio.run(test_telegram())
