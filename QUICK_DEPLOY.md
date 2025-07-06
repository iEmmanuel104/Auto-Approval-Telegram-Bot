# 🚀 Railway Multi-Bot Deploy Guide

## **30 Second Setup**

### **1. Setup .env file:**
```bash
cp env_simple.txt .env
# Edit .env with your bot credentials
```

### **2. Deploy on Railway:**
- **Deployment 1:** Set `BOT_OWNER=graceboy` (original bot)
- **Deployment 2:** Set `BOT_OWNER=policee` (trading room focus)  
- **Deployment 3:** Set `BOT_OWNER=wilfred` (personal touch)

### **3. Run:**
```bash
python bot.py
```

**Done!** Your bot now has the complete personality of that owner! 🎉

---

## **What Changes Between Bots:**

| Feature | Graceboy | Policee | Wilfred |
|---------|----------|---------|---------|
| **Welcome** | "This is the exact system that changed my life..." | "This is your shot to enter my trading room..." | "This is your shot to enter my trading room..." |
| **Support** | @graceboysupport | @policeesupport | @Wilfredsupport |
| **Guide** | t.me/graceboydeposit/3 | t.me/policeedeposit/4 | t.me/wilfreddeposit/3 |
| **Results** | t.me/Graceboytrading | t.me/policeethetrader | t.me/wilfredshaffa |
| **Personal** | @graceboylive | @policeeone | @Wilfredshaffa1 |
| **Code Word** | "GRACEBOY100" | "SIGNALROOMACCESS" | "SIGNALROOMACCESS" |

---

## **Add New Bot Owner:**

1. **Add to config.json:**
```json
{
  "your_name": {
    "bot_config": {
      "bot_name": "Your Trading Bot",
      "support_username": "yoursupport"
    },
    "messages": {
      "welcome_message": "Your custom welcome..."
    }
  }
}
```

2. **Deploy on Railway:**
- Create new Railway deployment
- Set `BOT_OWNER=your_name`
- Done! ✅

**That's it!** No code changes needed! 🔥 