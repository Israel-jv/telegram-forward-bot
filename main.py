import os
from threading import Thread
from flask import Flask
import bot  # your existing bot.py

# --- Flask server to keep the bot alive ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT"))  # Railway sets this automatically
    app.run(host="0.0.0.0", port=port)

# Start Flask in a thread
flask_thread = Thread(target=run_flask)
flask_thread.start()  # Do NOT make it daemon

# --- Run the bot ---
if __name__ == "__main__":
    print("✅ Web server starting...")
    
    try:
        bot.main()  # Make sure bot.py has a main() function
    except AttributeError:
        print("Bot started (assuming bot.py runs on import).")
    print("✅ Bot should now be running and Flask server live.")
