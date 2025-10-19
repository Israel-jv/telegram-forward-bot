from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, ConversationHandler, filters
)
import re

BOT_TOKEN = "8289064969:AAEyirLo6aM14HJYw2vgFHfkQP_T7kUubg8"
FORWARD_CHAT_ID = 6335294113  # your Telegram user ID

# Conversation states
QUESTION1, QUESTION2, QUESTION3 = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    first_name = user.first_name if user.first_name else "there"
    await update.message.reply_text(
        f"👋 እንኳን ደህና መጡ {first_name}!\n\n1️⃣ እባክዎ ሙሉ ስምዎን እና ስልክ ቁጥርዎን ያስገቡ።"
    )
    return QUESTION1

# Forward helper
async def forward_any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forward any type of message directly to admin chat and confirm to user."""
    try:
        await context.bot.forward_message(
            chat_id=FORWARD_CHAT_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
        await update.message.reply_text("✅ መልእክትዎ ተላከ።")
    except Exception as e:
        print(f"Error forwarding message: {e}")

# Check if text includes a phone number
def contains_phone_number(text: str) -> bool:
    return bool(re.search(r"\d{8,}", text))  # checks for 8+ digits

async def answer1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text or not contains_phone_number(text):
        await update.message.reply_text(
            "⚠️ እባክዎ ሙሉ ስምን እና ትክክለኛ ስልክ ቁጥር ያስገቡ።\n\nምሳሌ፦ አባተ አሮን 0912345678"
        )
        return QUESTION1

    await forward_any_message(update, context)
    context.user_data["name_phone"] = text
    await update.message.reply_text("2️⃣ አንድ ቀስ ያለ መዝሙር ይዘምሩ።")
    return QUESTION2

async def answer2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await forward_any_message(update, context)
    context.user_data["song"] = update.message.text or "🎤 Voice message"
    await update.message.reply_text("3️⃣ በናዝራዊያን በተለየ ማገልገል ምትፈልጉበት ዘርፍ ይጻፉ ወይም ይናገሩ።")
    return QUESTION3

async def answer3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await forward_any_message(update, context)
    context.user_data["service_area"] = update.message.text or "🎤 Voice message"

    name_phone = context.user_data["name_phone"]
    song = context.user_data["song"]
    service_area = context.user_data["service_area"]

    # Send summary to admin
    await context.bot.send_message(
        chat_id=FORWARD_CHAT_ID,
        text=(
            "📨 አዲስ መልእክት ተቀባይነት አግኝቷል:\n\n"
            f"👤 ስም እና ስልክ፦ {name_phone}\n"
            f"🎵 መዝሙር፦ {song}\n"
            f"🙏 ዘርፍ፦ {service_area}"
        )
    )

    await update.message.reply_text("ተባረኩ 🙏")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ውይይቱ ተሰርዟል።")
    return ConversationHandler.END

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            QUESTION1: [MessageHandler(filters.ALL & ~filters.COMMAND, answer1)],
            QUESTION2: [MessageHandler(filters.ALL & ~filters.COMMAND, answer2)],
            QUESTION3: [MessageHandler(filters.ALL & ~filters.COMMAND, answer3)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("✅ Bot is running...")
    app.run_polling()
