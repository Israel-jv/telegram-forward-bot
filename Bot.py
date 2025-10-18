import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Your bot token and chat ID to forward messages to
TOKEN = os.getenv("BOT_TOKEN")
FORWARD_CHAT_ID = int(os.getenv("FORWARD_CHAT_ID"))

# Async function to forward messages
async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        # Forward text messages
        if update.message.text:
            await context.bot.send_message(chat_id=FORWARD_CHAT_ID, text=update.message.text)

        # Forward voice messages
        if update.message.voice:
            await context.bot.forward_message(
                chat_id=FORWARD_CHAT_ID,
                from_chat_id=update.message.chat_id,
                message_id=update.message.message_id
            )

# Create the bot application
app = ApplicationBuilder().token(TOKEN).build()

# Add a handler for all types of messages
app.add_handler(MessageHandler(filters.ALL, forward_message))

# Start polling (async)
if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
