import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Get environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
FORWARD_CHAT_ID = int(os.getenv("FORWARD_CHAT_ID"))

# Async function to forward messages
async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await context.bot.forward_message(
            chat_id=FORWARD_CHAT_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )

# Build the bot application
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add a handler for all messages
app.add_handler(MessageHandler(filters.ALL, forward_message))

# Start polling (bot will run 24/7 on Render)
if __name__ == "__main__":
    app.run_polling()
