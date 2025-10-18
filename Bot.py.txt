from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from datetime import datetime
import pytz  # timezone library

# === Replace these with your info ===
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"   # from BotFather
OWNER_ID = 123456789                # your Telegram user ID
LOCAL_TIMEZONE = "Africa/Addis_Ababa"  # change if needed

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    user = update.effective_user
    name = user.full_name
    username = f"@{user.username}" if user.username else "(no username)"

    # Format the time
    now = datetime.now(pytz.timezone(LOCAL_TIMEZONE))
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")

    # Info message to send you
    info = (
        f"📩 *New message received!*\n\n"
        f"👤 From: {name}\n"
        f"🏷️ Username: {username}\n"
        f"🕒 Time: {time_str}\n"
    )

    # Forward the actual message
    await message.forward(chat_id=OWNER_ID)

    # Then send the info
    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=info,
        parse_mode="Markdown"
    )

    # Confirmation reply for the sender
    await message.reply_text("✅ Message received and forwarded!")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    print("🤖 Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
