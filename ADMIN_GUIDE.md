# Admin Guide - Graceboy Trading Bot

## 🔧 Configuration Setup

### 1. Environment Variables
Copy the `config.example.txt` file and rename it to `.env` (or set these as environment variables):

#### Required Variables:
```env
API_ID=1234567                    # Get from https://my.telegram.org
API_HASH=abcdef123456             # Get from https://my.telegram.org
BOT_TOKEN=123:ABC-DEF             # Get from @BotFather
CHID=-1001234567890              # Your channel ID (get from @userinfobot)
SUDO=123456789,987654321         # Admin user IDs (comma-separated)
MONGO_URI=mongodb://...          # MongoDB connection string
```

#### Customization Variables:
```env
BOT_NAME=Your Trading Bot Name
DEPOSIT_GUIDE_LINK=https://t.me/yourdeposit/3
RESULTS_CHANNEL_LINK=https://t.me/yourresults
SUPPORT_USERNAME=yoursupport
DIRECT_CONTACT_USERNAME=yourcontact
PROMO_CODE=YOURCODE100
```

### 2. Custom Messages
You can customize all bot messages using environment variables. See `config.example.txt` for examples.

---

## 📢 Admin Broadcast Commands

### `/bcast` - Broadcast Message
Sends a copy of the replied message to all bot users.

**How to use:**
1. Reply to any message in your bot's private chat
2. Type `/bcast`
3. The bot will send a copy of that message to all users

**Example:**
```
User: [Sends a photo with caption "New trading signal!"]
Admin: /bcast (as reply to the photo)
Bot: Sends the photo with caption to all users
```

### `/fcast` - Forward Message
Forwards the replied message to all bot users (shows "Forwarded from" label).

**How to use:**
1. Reply to any message in your bot's private chat
2. Type `/fcast`
3. The bot will forward that message to all users

**Example:**
```
User: [Sends a message "Trading results for today"]
Admin: /fcast (as reply to the message)
Bot: Forwards the message to all users with "Forwarded from" label
```

### `/users` - Get Statistics
Shows bot usage statistics including user count and group count.

**Response format:**
```
🍀 Chats Stats 🍀
🙋‍♂️ Users : 1,234
👥 Groups : 56
🚧 Total users & groups : 1,290
```

---

## 🎯 Broadcast Best Practices

### 1. Content Types You Can Broadcast:
- ✅ Text messages
- ✅ Photos with captions
- ✅ Videos with captions
- ✅ Documents
- ✅ Stickers
- ✅ Voice messages
- ✅ Messages with buttons/keyboards

### 2. Broadcast vs Forward:
- **Use `/bcast`** when you want to send as the bot (no forwarding label)
- **Use `/fcast`** when you want to show the original sender (with forwarding label)

### 3. Timing Considerations:
- Large broadcasts may take time to complete
- The bot will show progress and final statistics
- Failed messages are automatically handled and reported

### 4. Example Broadcast Results:
```
✅ Successfully sent to 1,180 users.
❌ Failed to send to 12 users.
👾 Found 23 blocked users
👻 Found 5 deactivated users.
```

---

## 👥 User Management

### Auto-Approval System
The bot automatically:
1. Approves join requests to your channel/group
2. Starts the onboarding flow for new users
3. Tracks user progress through the onboarding stages

### User States:
- **New User**: Just sent first message
- **Welcome Sent**: Received welcome message
- **Start Clicked**: Clicked /start button
- **Verified**: Passed channel subscription check
- **Setup Completed**: Confirmed account setup
- **Onboarding Complete**: Finished all steps

---

## 📊 Monitoring and Analytics

### Database Collections:
- `users`: All bot users
- `groups`: All groups/channels where bot is admin
- `onboarding`: User onboarding progress and timestamps

### Useful Queries (MongoDB):
```javascript
// Count users by onboarding stage
db.onboarding.aggregate([
  { $group: { _id: "$onboarding_stage", count: { $sum: 1 } } }
])

// Find users who need follow-up
db.onboarding.find({
  "setup_completed": false,
  "follow_up_1h_sent": false,
  "created_at": { $lt: new Date(Date.now() - 3600000) }
})
```

---

## 🔒 Security Notes

### Admin Access:
- Only users listed in `SUDO` can use admin commands
- Multiple admins can be set (comma-separated IDs)
- Admin commands only work in private chat with the bot

### User Privacy:
- The bot only stores user IDs and onboarding progress
- No personal information is stored beyond first names
- Users can be removed from database if they block the bot

---

## 🚀 Quick Start Checklist

1. **Setup Environment:**
   - [ ] Set all required environment variables
   - [ ] Configure MongoDB database
   - [ ] Set admin user IDs in SUDO

2. **Test Bot:**
   - [ ] Start the bot: `python bot.py`
   - [ ] Test with a new user account
   - [ ] Verify onboarding flow works

3. **Configure Channel:**
   - [ ] Add bot to your channel as admin
   - [ ] Give bot "Add members" permission
   - [ ] Set channel ID in CHID variable

4. **Test Broadcasting:**
   - [ ] Send `/users` to check statistics
   - [ ] Test `/bcast` with a sample message
   - [ ] Test `/fcast` with a sample message

---

## 🔧 Troubleshooting

### Common Issues:

**"Make Sure I Am Admin In Your Channel"**
- Bot is not admin in the channel specified in CHID
- Bot doesn't have "Add members" permission

**Broadcast not working:**
- Check if you're replying to a message when using `/bcast` or `/fcast`
- Verify you're an admin (ID in SUDO list)

**Follow-ups not sending:**
- Check if scheduler is running (should see "Scheduler started" in logs)
- Verify MongoDB connection is working

**Environment variables not loading:**
- Make sure `.env` file is in the same directory as `bot.py`
- Check for typos in variable names

### Support:
If you encounter issues, check the bot logs for detailed error messages. The bot provides comprehensive logging for debugging purposes. 