from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

BOT_TOKEN = "8289064969:AAEyirLo6aM14HJYw2vgFHfkQP_T7kUubg8"
FORWARD_CHAT_ID = 6335294113  # your Telegram user ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    first_name = user.first_name if user.first_name else "there"
    await update.message.reply_text(
        f"👋 Welcome , {first_name}! \n አንድ ቀስ ያለ መዝሙር::\n በናዝራዊያን በተለየ ማገልገል ምትፈልጉበት ዘርፍ::\n \n ተባረኩ"
    )

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await context.bot.forward_message(
            chat_id=FORWARD_CHAT_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, forward_message))

    print("✅ Bot is running...")
    app.run_polling()
