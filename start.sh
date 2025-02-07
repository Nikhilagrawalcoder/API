#!/bin/bash

# Update system and install necessary dependencies for Chromium
apt-get update
apt-get install -y chromium
apt-get install -y chromium-driver

# Set environment variables for Chrome and Chromedriver
export CHROME_BIN=/usr/bin/chromium
export CHROME_DRIVER=/usr/lib/chromium-browser/chromedriver

# Start the Flask application using Gunicorn
gunicorn -b 0.0.0.0:10000 app:app
