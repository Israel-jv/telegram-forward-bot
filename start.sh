#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Upgrade pip and install dependencies inside the venv
pip install --upgrade pip
pip install -r requirements.txt

# Run the bot using the venv's python
venv/bin/python Bot.py
