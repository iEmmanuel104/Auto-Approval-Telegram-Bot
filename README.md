# Auto Approval Telegram Bot

A Telegram bot that automatically approves chat join requests for groups and channels. Built with Python and Pyrogram.

## Features

- ✅ Auto-approve chat join requests
- 📊 User and group statistics
- 📢 Broadcast messages to all users
- 🔐 Force subscribe to channel
- 💾 MongoDB database integration
- 🎛️ Admin controls

## Environment Variables

Set these environment variables in your deployment platform:

```env
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
BOT_TOKEN=your_bot_token
CHID=your_channel_id
SUDO=your_admin_user_id
MONGO_URI=your_mongodb_connection_string
CHANNEL_URL=https://t.me/your_channel
SUPPORT_URL=https://t.me/your_support
```

### Getting Environment Variables

1. **API_ID & API_HASH**: 
   - Go to [my.telegram.org](https://my.telegram.org)
   - Log in with your phone number
   - Create a new application
   - Copy API_ID and API_HASH

2. **BOT_TOKEN**: 
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Create a new bot with `/newbot`
   - Copy the bot token

3. **CHID**: 
   - Your channel ID where users must subscribe
   - Make the bot admin in this channel

4. **SUDO**: 
   - Your Telegram user ID (for admin access)
   - You can get this by messaging [@userinfobot](https://t.me/userinfobot)

5. **MONGO_URI**: 
   - MongoDB connection string
   - Get free MongoDB at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

## Railway Deployment

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. Click the "Deploy on Railway" button
2. Connect your GitHub account
3. Set the environment variables in Railway dashboard
4. Deploy!

### Manual Railway Deployment

1. Fork this repository
2. Connect your GitHub account to Railway
3. Create a new project and connect your forked repository
4. Set environment variables:
   - Go to your project settings
   - Add all required environment variables
5. Deploy

## Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Auto-Approval-Telegram-Bot.git
   cd Auto-Approval-Telegram-Bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables:
   ```bash
   export API_ID=your_api_id
   export API_HASH=your_api_hash
   export BOT_TOKEN=your_bot_token
   export CHID=your_channel_id
   export SUDO=your_user_id
   export MONGO_URI=your_mongodb_uri
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

## Bot Commands

- `/start` - Start the bot
- `/users` - Get user statistics (admin only)
- `/bcast` - Broadcast message to all users (admin only)
- `/fcast` - Forward message to all users (admin only)

## Setup Instructions

1. Add the bot to your group/channel
2. Make the bot admin with "Add Members" permission
3. Users who request to join will be automatically approved
4. The bot will send a welcome message to approved users

## File Structure

```
Auto-Approval-Telegram-Bot/
├── bot.py              # Main bot file
├── configs.py          # Configuration management
├── database.py         # Database operations
├── requirements.txt    # Python dependencies
├── Procfile           # Railway/Heroku deployment
├── runtime.txt        # Python version
└── README.md          # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, join our [Telegram Channel](https://t.me/AutoBot) or contact [@AutoBot](https://t.me/AutoBot).

## Disclaimer

This bot is for educational purposes. Make sure to comply with Telegram's Terms of Service and your local laws when using this bot.