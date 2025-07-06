# 🎯 Namespace-Based Multi-Bot System

**The Simplest Way to Deploy Multiple Bot Personalities**

---

## 🚀 **How It Works**

1. **One JSON file** (`config.json`) with multiple namespaces
2. **One environment variable** (`BOT_OWNER`) to select which bot to run
3. **Zero code changes** needed for different deployments

---

## ⚡ **Quick Start**

### **1. Setup Environment**
```bash
# Copy template
cp env_simple.txt .env

# Edit with your credentials
BOT_OWNER=graceboy  # or policee or wilfred
API_ID=1234567
API_HASH=your_hash
BOT_TOKEN=your_token
# ... etc
```

### **2. Deploy Any Bot**
**On Railway (or similar platforms):**
- Create 3 separate Railway deployments
- Set `BOT_OWNER` environment variable differently in each:
  - Deployment 1: `BOT_OWNER=graceboy`
  - Deployment 2: `BOT_OWNER=policee` 
  - Deployment 3: `BOT_OWNER=wilfred`

### **3. Run Bot**
```bash
python bot.py
```

---

## 🎨 **Available Bot Personalities**

| Owner | Bot Name | Style | Support | Results Channel |
|-------|----------|-------|---------|-----------------|
| **graceboy** | Graceboy Trading Bot | Professional, Proven | @graceboysupport | @Graceboytrading |
| **policee** | Policee Trading Room Bot | Energetic, Room-based | @policeesupport | @policeethetrader |
| **wilfred** | Wilfred Trading Room Bot | Personal, Engaging | @Wilfredsupport | @wilfredshaffa |

---

## 📋 **Configuration Structure**

```json
{
  "graceboy": {
    "bot_config": { ... },
    "timing": { ... },
    "messages": { ... }
  },
  "policee": {
    "bot_config": { ... },
    "timing": { ... }, 
    "messages": { ... }
  },
  "wilfred": {
    "bot_config": { ... },
    "timing": { ... },
    "messages": { ... }
  }
}
```

---

## ✨ **Adding New Bot Owners**

1. **Add new namespace to `config.json`:**
```json
{
  "your_new_owner": {
    "bot_config": {
      "bot_name": "Your Bot Name",
      "support_username": "yoursupport",
      "deposit_guide_link": "https://t.me/yourguide",
      // ... etc
    },
    "messages": {
      "welcome_message": "Your custom welcome...",
      // ... etc
    }
  }
}
```

2. **Deploy the new bot:**
- Create new Railway deployment  
- Set `BOT_OWNER=your_new_owner`
- Deploy! ✅

**That's it!** 🎉

---

## 🔧 **Railway Deployment**

### **Environment Variables**
Set these in each Railway deployment:
```env
BOT_OWNER=graceboy          # For Graceboy bot
BOT_OWNER=policee           # For Policee bot  
BOT_OWNER=wilfred           # For Wilfred bot
```

### **Local Testing**
```bash
python bot.py               # Run with current BOT_OWNER
BOT_OWNER=policee python bot.py  # Override for this session
```

---

## 💡 **Benefits**

✅ **One codebase** - Same bot logic for all deployments  
✅ **Easy switching** - Change personality with one variable  
✅ **No file juggling** - Everything in one config.json  
✅ **Scalable** - Add unlimited bot owners  
✅ **No parsing issues** - JSON handles multi-line perfectly  
✅ **Environment friendly** - Works with Docker, Railway, etc.  

---

## 🔄 **Migration from Old System**

If you had multiple config files before:

```bash
# Old way (multiple files + multiple deployments)
# - config_graceboy.json
# - config_policee.json  
# - config_wilfred.json

# New way (one config.json + environment variable)
# Just set BOT_OWNER in Railway environment variables
```

---

## 🚨 **Important Notes**

- **Required in .env**: `API_ID`, `API_HASH`, `BOT_TOKEN`, `CHID`, `SUDO`, `MONGO_URI`, `BOT_OWNER`
- **Optional in .env**: `FOLLOW_UP_1_MINUTES`, `FOLLOW_UP_3_MINUTES`
- **Everything else**: Configured in `config.json` namespaces

---

## 🎯 **Example Railway Deployment**

**Step 1:** Create Railway project from your GitHub repo

**Step 2:** Set environment variables in Railway dashboard:
```env
API_ID=1234567
API_HASH=abcdef123456
BOT_TOKEN=1234567890:ABC-DEF
CHID=-1001234567890
SUDO=123456789
MONGO_URI=mongodb+srv://...
BOT_OWNER=policee
```

**Step 3:** Deploy! ✅

**Result:** Your bot now runs with Policee's messages and branding automatically!

**Perfect for agencies running multiple trading bots!** 🚀 