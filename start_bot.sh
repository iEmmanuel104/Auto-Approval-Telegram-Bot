#!/bin/bash

# Auto Approval Bot Starter Script

echo "🤖 Starting Auto Approval Bot..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.example to .env and fill in your credentials"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! python -c "import pyrogram" 2>/dev/null; then
    echo "📥 Installing requirements..."
    pip install -r requirements.txt
fi

# Export environment variables
echo "🔧 Loading environment variables..."
export $(cat .env | grep -v '^#' | xargs)

# Start the bot
echo "🚀 Starting bot..."
python bot.py