#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 not found. Please install Python 3."
    exit 1
fi

# Create and activate virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Start the Flask app
python src/app.py