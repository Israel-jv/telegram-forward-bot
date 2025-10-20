# main.py
import os
from threading import Thread
from flask import Flask
import bot  # your existing bot.py file

# --- Simple Flask server to keep the bot alive ---
app = Flask(__name__)


@app.route('/')
def home():
    return "Bot is alive!"  # UptimeRobot will see this


def run_flask():
    # Replit uses PORT environment variable; default to 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


# --- Start the web server in a separate thread ---
def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True  # ensures Flask thread exits if bot stops
    t.start()


# --- Run the bot and the webserver together ---
if __name__ == "__main__":
    keep_alive()
    print("✅ Web server running... Now starting bot.")

    # --- Run your bot.py main function ---
    # Make sure bot.py has something like:
    # if __name__ == "__main__":
    #     app.run_polling()
    # If not, call the polling function here directly
    try:
        # If your bot.py has a function called main() to start the bot
        bot.main()
    except AttributeError:
        # fallback: maybe your bot.py runs automatically on import
        print("Bot started (assuming bot.py runs on import).")

    print("Bot should now be running and Flask server is live.")


