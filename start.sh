#!/bin/bash

# Install Chromium
apt-get update
apt-get install -y chromium

# Set the Chrome binary path
export CHROME_BIN=/usr/bin/chromium

# Start the Flask app with Gunicorn
gunicorn -b 0.0.0.0:10000 app:app
