
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

print("BOT_TOKEN from env:", os.getenv("BOT_TOKEN"))
print("FORWARD_CHAT_ID from env:", os.getenv("FORWARD_CHAT_ID"))

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

FORWARD_CHAT_ID_STR = os.getenv("FORWARD_CHAT_ID")
if not FORWARD_CHAT_ID_STR:
    raise ValueError("FORWARD_CHAT_ID environment variable is not set")
FORWARD_CHAT_ID = int(FORWARD_CHAT_ID_STR)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("✅ Bot is running and ready to forward messages!")

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and (update.message.text or update.message.voice):
        await context.bot.forward_message(
            chat_id=FORWARD_CHAT_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT | filters.VOICE, forward_message))
    app.run_polling()

