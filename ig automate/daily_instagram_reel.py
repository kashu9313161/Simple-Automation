import os
import sys
import time
import schedule
from instagrapi import Client
from dotenv import load_dotenv
import asyncio
from telegram import Bot
from pathlib import Path

# ----------------- Debug / Startup -----------------
print("🚀 Script started...")

# ----------------- Load Environment Variables -----------------
env_path = Path(__file__).parent / ".env"
if not env_path.exists():
    print(f"❌ .env file not found at {env_path}")
    sys.exit(1)
else:
    load_dotenv(dotenv_path=env_path)
    print(f"✅ Loaded .env from: {env_path}")

# Retrieve variables
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Debug prints
print(f"Instagram username: {INSTAGRAM_USERNAME}")
print(f"Instagram password: {'***' if INSTAGRAM_PASSWORD else None}")
print(f"Telegram bot token: {TELEGRAM_BOT_TOKEN}")
print(f"Telegram chat ID: {TELEGRAM_CHAT_ID}")

# Exit if any variable missing
missing_vars = []
if not INSTAGRAM_USERNAME or not INSTAGRAM_PASSWORD:
    missing_vars.append("Instagram credentials")
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    missing_vars.append("Telegram credentials")

if missing_vars:
    print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
    sys.exit(1)

print("✅ All environment variables loaded successfully!")

# ----------------- Telegram Notification -----------------
async def send_telegram(message: str):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        print(f"📩 Telegram message sent: {message}")
    except Exception as e:
        print(f"⚠️ Telegram error: {e}")

def notify(message: str):
    asyncio.run(send_telegram(message))

# ----------------- Instagram Login -----------------
def login_instagram():
    print("🔑 Logging into Instagram...")
    cl = Client()
    session_file = "session.json"

    try:
        if os.path.exists(session_file):
            cl.load_settings(session_file)
            cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            print("✅ Logged in using saved session.")
        else:
            cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            cl.dump_settings(session_file)
            print("✅ Logged in fresh and session saved.")
        return cl
    except Exception as e:
        notify(f"❌ Instagram login failed: {e}")
        print(f"❌ Instagram login failed: {e}")
        raise

# ----------------- Reel Upload -----------------
def upload_reel():
    print("🎬 Starting reel upload...")
    try:
        cl = login_instagram()
        video_path = "reel.mp4"  # Make sure this file exists in the same folder

        caption = (
            "💬 “Want YOUR reel to stay trending for DAYS? 👀✨ "
            "DM us now & let’s boost your reach 🚀”\n"
            "#motivationalquotesdaily #dreamcore "
            "#ReelBoost #ReelPromotion #ReelGrowth #InstaGrowth #ViralReels #ReelsOnTop "
            "#AdvertiseWithUs #SocialMediaMarketing #ReelAds #DigitalMarketing #GrowWithReels #PromoteYourReel "
            "#SmallBusinessSupport #BrandVisibility #BusinessGrowth #ContentPromotion #OnlineGrowth "
            "#TrendingNow #ReachMorePeople #ExplorePage #StayTrending #MoreViewsMoreReach"
        )

        cl.clip_upload(video_path, caption)
        print("🎉 Reel uploaded successfully!")
        notify("✅ Reel uploaded successfully!")
    except Exception as e:
        print(f"❌ Error uploading reel: {e}")
        notify(f"❌ Error uploading reel: {e}")

# ----------------- Main Scheduling -----------------
def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() == "now":
        print("🤖 Bot started in NOW mode...")
        upload_reel()
    else:
        print("🤖 Bot started. Waiting for schedule...")
        schedule.every().day.at("14:30").do(upload_reel)
        notify("🤖 Instagram automation started. Reel will upload daily at 11:00 AM.")

        while True:
            schedule.run_pending()
            time.sleep(30)

# ----------------- Run Script -----------------
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"💥 Script crashed: {e}")
