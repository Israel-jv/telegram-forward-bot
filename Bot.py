import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Load token and chat ID
TOKEN = os.getenv("BOT_TOKEN")
FORWARD_CHAT_ID = int(os.getenv("FORWARD_CHAT_ID"))

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running!")

# Forward text or voice messages
async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and (update.message.text or update.message.voice):
        await context.bot.forward_message(
            chat_id=FORWARD_CHAT_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )

# Build app
app = ApplicationBuilder().token(TOKEN).build()

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT | filters.VOICE, forward_message))

# Run bot
if __name__ == "__main__":
    app.run_polling()
