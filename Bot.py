import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN") or "YOUR_BOT_TOKEN_HERE"
FORWARD_CHAT_ID = os.getenv("FORWARD_CHAT_ID") or "YOUR_CHAT_ID_HERE"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        if update.message.voice:
            await context.bot.forward_message(
                chat_id=FORWARD_CHAT_ID,
                from_chat_id=update.message.chat_id,
                message_id=update.message.message_id
            )
        elif update.message.text:
            await context.bot.send_message(
                chat_id=FORWARD_CHAT_ID,
                text=f"Message from {update.message.from_user.first_name}:\n{update.message.text}"
            )

if __name__ == "__main__":
    import asyncio

    async def main():
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(MessageHandler(filters.ALL, handle_message))

        print("Bot is running...")
        await app.run_polling(allowed_updates=Update.ALL_TYPES)

    # Ensures Render shuts down gracefully
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "Cannot close a running event loop" not in str(e):
            raise
