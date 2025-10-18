import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

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
            sender = update.message.from_user.username or "Unknown"
            text = f"📩 Message from @{sender}:\n\n{update.message.text}"
            await context.bot.send_message(chat_id=FORWARD_CHAT_ID, text=text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.VOICE, forward_message))
    print("🤖 Bot is running...")
    app.run_polling()
