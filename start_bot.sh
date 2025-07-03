#!/bin/bash

# Auto Approval Bot Starter Script

echo "🤖 Starting Auto Approval Bot..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with your bot credentials"
    echo "Copy .env.example to .env and fill in your values"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
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
export $(cat .env | grep -v '^#' | grep -v '^$' | xargs)

# Start the bot
echo "🚀 Starting bot..."
python bot.py