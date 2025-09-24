import asyncio
from telegram import Bot

# 🔹 Replace with your actual values
TOKEN = "8421036755:AAE5OyCn3DAHeySVq84ZXs4EA-CouGc1gGw"
CHAT_ID = "1608888400"

async def main():
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="✅ Telegram bot is working fine!")

if __name__ == "__main__":
    asyncio.run(main())
