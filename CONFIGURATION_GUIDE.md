# 🎯 Multi-Bot Configuration Guide

## 🚀 **Multiple Deployment Solutions**

Perfect for deploying the same bot with different branding/messages for different audiences!

---

## ✅ **Solution 1: JSON Configuration (Recommended)**

### **How it Works:**
- Each bot deployment uses a different `config.json` file
- No environment variable parsing issues
- Easy to edit and maintain
- Clean separation of concerns

### **Setup Steps:**

1. **For Each Bot Deployment:**
   ```bash
   # Bot 1 (Graceboy Trading)
   cp config.json config_graceboy.json
   
   # Bot 2 (Premium Trading)  
   cp config_bot1.json config_premium.json
   
   # Bot 3 (Elite Forex)
   cp config_bot2.json config_elite.json
   ```

2. **Deploy Each Bot:**
   ```bash
   # Deploy Bot 1
   cp config_graceboy.json config.json
   python bot.py
   
   # Deploy Bot 2  
   cp config_premium.json config.json
   python bot.py
   
   # Deploy Bot 3
   cp config_elite.json config.json  
   python bot.py
   ```

3. **Your .env file only needs essentials:**
   ```env
   API_ID=1234567
   API_HASH=abcdef123456
   BOT_TOKEN=1234567890:ABC-DEF1234567890
   CHID=-1001234567890
   SUDO=123456789
   MONGO_URI=mongodb+srv://...
   ```

---

## ⚡ **Solution 2: Environment Variable Selection**

### **Setup Steps:**

1. **Create Multiple .env Files:**
   ```bash
   # .env.graceboy
   # .env.premium  
   # .env.elite
   ```

2. **Use CONFIG_NAME Environment Variable:**
   ```bash
   CONFIG_NAME=graceboy python bot.py
   CONFIG_NAME=premium python bot.py
   CONFIG_NAME=elite python bot.py
   ```

---

## 🎨 **Solution 3: Database Configuration**

### **For Dynamic Updates Without Redeployment:**

1. **Store messages in MongoDB**
2. **Update via admin commands**
3. **Real-time message changes**

---

## 📋 **Configuration Examples**

### **Graceboy Trading (Original):**
```json
{
  "bot_config": {
    "bot_name": "Graceboy Trading Bot",
    "support_username": "graceboysupport",
    "promo_code": "GRACEBOY100"
  },
  "messages": {
    "welcome_message": "Welcome, {first_name}!\n\nThis is the exact system that changed my life..."
  }
}
```

### **Premium Trading (Upscale):**
```json
{
  "bot_config": {
    "bot_name": "Premium Trading Signals Bot", 
    "support_username": "premiumsupport",
    "promo_code": "PREMIUM100"
  },
  "messages": {
    "welcome_message": "Welcome to Premium Trading, {first_name}! 🚀\n\nYou've just unlocked access to our EXCLUSIVE premium trading signals..."
  }
}
```

### **Elite Forex (High-End):**
```json
{
  "bot_config": {
    "bot_name": "Elite Forex Master Bot",
    "support_username": "eliteforexsupport", 
    "promo_code": "ELITE200"
  },
  "messages": {
    "welcome_message": "Greetings, {first_name}! 💎\n\nYou have been selected for our ELITE forex trading program..."
  }
}
```

---

## 🔧 **Quick Deployment Commands**

### **Deploy Graceboy Bot:**
```bash
cp config.json config_active.json && mv config_active.json config.json
python bot.py
```

### **Deploy Premium Bot:**
```bash
cp config_bot1.json config.json  
python bot.py
```

### **Deploy Elite Bot:**
```bash
cp config_bot2.json config.json
python bot.py
```

---

## 📊 **Benefits Comparison**

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **JSON Config** | ✅ No parsing issues<br>✅ Easy to edit<br>✅ Clean separation | ❌ File management | Multiple deployments |
| **Environment Variables** | ✅ 12-factor app compliant<br>✅ Container friendly | ❌ Parsing issues<br>❌ Complex setup | Single deployment |
| **Database Config** | ✅ Dynamic updates<br>✅ No redeployment needed | ❌ More complex<br>❌ Database dependency | Live updates needed |

---

## 🎯 **Recommended Workflow**

### **For 3 Different Bot Deployments:**

1. **Create your configs:**
   - `config_graceboy.json` - Original branding
   - `config_premium.json` - Premium branding  
   - `config_elite.json` - Elite branding

2. **Deploy separately:**
   ```bash
   # Server 1
   cp config_graceboy.json config.json && python bot.py
   
   # Server 2  
   cp config_premium.json config.json && python bot.py
   
   # Server 3
   cp config_elite.json config.json && python bot.py
   ```

3. **Update messages:**
   - Edit the respective JSON file
   - Restart the bot
   - No code changes needed!

---

## 🚨 **Important Notes**

### **Required Environment Variables:**
These must ALWAYS be set (not in JSON):
- `API_ID`, `API_HASH`, `BOT_TOKEN`
- `CHID`, `SUDO`, `MONGO_URI`

### **Optional in JSON:**
Everything else can be customized per deployment:
- All messages and branding
- Links and usernames  
- Timing configuration
- Bot names

### **Testing:**
Use `"follow_up_1_minutes": 1, "follow_up_3_minutes": 3` for testing.
For production: `"follow_up_1_minutes": 60, "follow_up_3_minutes": 180`

---

## ✅ **Quick Test**

1. **Copy one of the example configs:**
   ```bash
   cp config_bot1.json config.json
   ```

2. **Run your bot:**
   ```bash
   python bot.py
   ```

3. **You should see:**
   ```
   ✅ JSON configuration loaded successfully
   🤖 Premium Trading Signals Bot is starting...
   ```

4. **Test the messages** - they'll be completely different from the original!

This approach gives you **complete flexibility** to run the same bot code with totally different branding and messaging for different target audiences! 🎉 