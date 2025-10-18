import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
FORWARD_CHAT_ID = int(os.getenv("FORWARD_CHAT_ID"))

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        if update.message.text:
            await context.bot.send_message(chat_id=FORWARD_CHAT_ID, text=update.message.text)
        if update.message.voice:
            await context.bot.forward_message(chat_id=FORWARD_CHAT_ID,
                                              from_chat_id=update.message.chat_id,
                                              message_id=update.message.message_id)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, forward_message))

if __name__ == "__main__":
    app.run_polling()
