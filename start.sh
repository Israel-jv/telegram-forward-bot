#!/bin/bash
# Remove old caches just in case
rm -rf .venv __pycache__ 

# Install dependencies fresh
pip install -r requirements.txt

# Start the bot
python Bot.py
