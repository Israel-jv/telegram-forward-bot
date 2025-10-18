from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os
import asyncio

# Get token and chat ID from environment variables
TOKEN = os.getenv("BOT_TOKEN")
FORWARD_CHAT_ID = int(os.getenv("FORWARD_CHAT_ID"))

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forward text and voice messages to your chat ID."""
    if update.message:
        if update.message.voice:
            await context.bot.forward_message(
                chat_id=FORWARD_CHAT_ID,
                from_chat_id=update.message.chat_id,
                message_id=update.message.message_id
            )
        elif update.message.text:
            text = f"📩 From @{update.message.from_user.username or 'Unknown'}:\n{update.message.text}"
            await context.bot.send_message(chat_id=FORWARD_CHAT_ID, text=text)

async def main():
    print("🚀 Bot is starting...")
    application = ApplicationBuilder().token(TOKEN).build()

    # Handle both voice and text
    application.add_handler(MessageHandler(filters.TEXT | filters.VOICE, forward_message))

    print("🤖 Bot is running...")
    await application.run_polling()  # <-- this keeps it alive

if __name__ == "__main__":
    asyncio.run(main())
