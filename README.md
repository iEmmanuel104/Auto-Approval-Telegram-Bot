# Auto Approval Bot Setup Guide

## Bot Overview

This is a Telegram bot that automatically approves join requests for channels/groups. Here's what it does:

### Main Features:
1. **Auto-Approval**: Automatically approves join requests when users request to join a channel/group
2. **Force Subscribe**: Requires users to join a specific channel before using the bot
3. **Welcome Messages**: Sends welcome messages to newly approved users
4. **Admin Commands**: 
   - `/users` - Shows stats of users and groups
   - `/bcast` - Broadcast messages to all users
   - `/fcast` - Forward messages to all users

### How the Bot Works:
1. When someone requests to join a channel/group where the bot is admin, it automatically approves them
2. The bot sends a welcome message to the approved user
3. Users must first join the force subscribe channel to use the bot
4. All user and group data is stored in MongoDB

## Setup Instructions

### Prerequisites:
1. Python 3.8+ with pip installed
2. MongoDB database (local or cloud like MongoDB Atlas)
3. Telegram API credentials from https://my.telegram.org
4. A Telegram Bot Token from @BotFather

### Step 1: Install Dependencies
```bash
# Install pip if not already installed
sudo apt update
sudo apt install python3-pip python3-venv

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your values:

#### Getting API_ID and API_HASH:
1. Go to https://my.telegram.org
2. Log in with your Telegram phone number
3. You'll receive a confirmation code on Telegram - enter it
4. Click on "API development tools"
5. If you haven't created an app yet:
   - Fill in the form:
     - **App title**: Choose any name (e.g., "My Bot")
     - **Short name**: 5-32 characters (e.g., "mybot")
     - **Platform**: Choose "Other"
     - **Description**: Optional
   - Click "Create application"
6. You'll see your credentials:
   - **App api_id**: This is your `API_ID` (it's a number like 12345678)
   - **App api_hash**: This is your `API_HASH` (it's a 32-character string)

#### Getting BOT_TOKEN:
1. Open Telegram and search for @BotFather
2. Start a chat and send `/newbot`
3. Choose a name for your bot (e.g., "Auto Approver")
4. Choose a username for your bot (must end with 'bot', e.g., "auto_approve_bot")
5. BotFather will give you a token like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
6. This is your `BOT_TOKEN`

#### Getting CHID (Channel ID):
**Method 1 - Using a Bot:**
1. Add @getidsbot to your channel as admin
2. Forward any message from your channel to @getidsbot
3. The bot will reply with the channel ID (it will be a negative number like -1001234567890)
4. Remove @getidsbot from your channel after getting the ID

**Method 2 - Using Web Telegram:**
1. Go to https://web.telegram.org
2. Open your channel
3. Look at the URL: `https://web.telegram.org/k/#-1234567890`
4. The number after # is your channel ID (include the minus sign)

**Important**: After getting the CHID, make your bot admin in this channel with permissions:
- Add Members
- Manage Join Requests

#### Getting SUDO (Your User ID):
1. Open Telegram and search for @userinfobot or @getidsbot
2. Start the bot and it will show your user ID
3. It will be a number like 123456789
4. For multiple admins, separate IDs with spaces: `123456789 987654321`

#### Getting CHANNEL_URL and SUPPORT_URL:
- `CHANNEL_URL`: The URL of your main channel (e.g., https://t.me/YourChannel)
- `SUPPORT_URL`: The URL of your support group (e.g., https://t.me/YourSupportGroup)
- These URLs will be shown as buttons when users interact with the bot

#### Example .env file:
```
API_ID=12345678
API_HASH=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
CHID=-1001234567890
SUDO=123456789
MONGO_URI=your_mongodb_connection_string
CHANNEL_URL=https://t.me/YourChannel
SUPPORT_URL=https://t.me/YourSupportGroup
```

### Step 3: Set Up the Bot
1. Create a bot via @BotFather and get the bot token
2. Add the bot to your channel/group as admin with these permissions:
   - Add Members
   - Manage Join Requests
3. Get your channel ID (you can use @getidsbot)
4. Make sure MongoDB is running

### Step 4: Run the Bot
```bash
# With virtual environment activated
python bot.py
```

You should see "I'm Alive Now!" when the bot starts successfully.

### Step 5: Test the Bot
1. Start the bot by sending `/start` in private chat
2. The bot will ask you to join the force subscribe channel
3. Once joined, you can use the bot
4. Try joining a channel/group where the bot is admin - it should auto-approve you

## Additional Notes:
- The Flask app (`app.py`) is for deployment on platforms like Heroku
- The bot stores user and group IDs in MongoDB for statistics and broadcasting
- Make sure to keep your credentials secure and never commit them to Git

# Quick Start Guide - Auto Approval Bot

## ✅ Setup Completed!

I've set up everything for you. Here's what's been done:

1. ✅ Created virtual environment (`venv/`)
2. ✅ Installed pip and dependencies
3. ✅ Created `.env` file for configuration
4. ✅ Created start scripts for both Linux/Mac and Windows

## 🚀 To Start the Bot:

### Step 1: Configure the Bot
Edit the `.env` file and fill in your credentials:

```bash
# Edit this file
nano .env  # or use any text editor
```

You need to provide:

**API_ID & API_HASH** (from https://my.telegram.org):
- Log in with your phone number → API development tools
- Create new application if needed (Platform: "Other")
- Copy the App api_id (number) and App api_hash (32-char string)

**BOT_TOKEN** (from @BotFather):
- Send `/newbot` → Choose name → Choose username (must end with 'bot')
- Copy the token (format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

**CHID** (Channel ID):
- Add @getidsbot to your channel → Forward any message to it
- Copy the negative number (like -1001234567890)
- Make your bot admin with "Add Members" and "Manage Join Requests" permissions

**SUDO** (Your User ID):
- Message @userinfobot or @getidsbot
- Copy your user ID (number like 123456789)
- For multiple admins use spaces: `123456789 987654321`

**MONGO_URI** - MongoDB connection string

**CHANNEL_URL** - Your main channel URL (e.g., https://t.me/YourChannel)

**SUPPORT_URL** - Your support group URL (e.g., https://t.me/YourSupportGroup)

### Step 2: Complete Package Installation
Since the installation timed out, run this to complete it:

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Complete installation
pip install -r requirements.txt
```

### Step 3: Start the Bot

**On Linux/Mac:**
```bash
./start_bot.sh
```

**On Windows:**
```cmd
start_bot.bat
```

**Or manually:**
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python bot.py
```

## 📝 Important Notes:

1. Make sure MongoDB is running before starting the bot
2. The bot must be admin in your channel with these permissions:
   - Add Members
   - Manage Join Requests
3. Users must join your force subscribe channel before using the bot

## 🛠️ Troubleshooting:

If you encounter any issues:
1. Make sure all packages are installed: `pip install -r requirements.txt`
2. Check that your `.env` file has all required values
3. Ensure MongoDB is accessible
4. Verify the bot is admin in your channel

## 📖 Bot Commands:
- `/start` - Start the bot (users)
- `/users` - Show statistics (admin only)
- `/bcast` - Broadcast message to all users (admin only)
- `/fcast` - Forward message to all users (admin only)