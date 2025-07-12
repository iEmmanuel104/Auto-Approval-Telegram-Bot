import os
import json
from typing import List
from pathlib import Path

class Config:
    def __init__(self):
        # Load JSON configuration first
        self._load_json_config()
        
        # Load environment variables (required)
        self._load_env_config()
    
    def _load_json_config(self):
        """Load configuration from JSON file"""
        config_file = Path("config.json")
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.json_config = json.load(f)
                print("✅ JSON configuration loaded successfully")
            except Exception as e:
                print(f"⚠️ Error loading JSON config: {e}")
                self.json_config = {}
        else:
            print("⚠️ No config.json found, using environment variables and defaults")
            self.json_config = {}
    
    def _load_env_config(self):
        """Load environment variables"""
        # Required environment variables
        self.API_ID: int = int(os.getenv("API_ID", "0"))
        self.API_HASH: str = os.getenv("API_HASH", "")
        self.BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
        
        # Force Subscribe Channel ID
        self.CHID: int = int(os.getenv("CHID", "0"))
        
        # Admin/Owner User IDs (can be comma-separated)
        self.SUDO: List[int] = []
        if os.getenv("SUDO"):
            self.SUDO = [int(x.strip()) for x in os.getenv("SUDO").split(",")]
        
        # Database Configuration
        self.MONGO_URI: str = os.getenv("MONGO_URI", "")
        self.DB_NAME: str = os.getenv("DB_NAME", "main")
        
        # Bot Owner Configuration
        self.BOT_OWNER: str = os.getenv("BOT_OWNER", "graceboy")
        
        # Load configuration from JSON using bot owner namespace
        owner_config = self.json_config.get(self.BOT_OWNER, {})
        bot_config = owner_config.get("bot_config", {})
        timing_config = owner_config.get("timing", {})
        messages_config = owner_config.get("messages", {})
        
        if not owner_config:
            print(f"⚠️  Warning: No configuration found for BOT_OWNER='{self.BOT_OWNER}'")
            print(f"Available owners: {list(self.json_config.keys())}")
            print("Using fallback configuration...")
        
        # Bot Configuration
        self.BOT_NAME: str = bot_config.get("bot_name", os.getenv("BOT_NAME", "Graceboy Trading Bot"))
        
        # Optional URLs
        self.CHANNEL_URL: str = bot_config.get("channel_url", os.getenv("CHANNEL_URL", "https://t.me/xxxx"))
        self.SUPPORT_URL: str = bot_config.get("support_url", os.getenv("SUPPORT_URL", "https://t.me/xxxx"))
        
        # Trading Links
        self.DEPOSIT_GUIDE_LINK: str = bot_config.get("deposit_guide_link", os.getenv("DEPOSIT_GUIDE_LINK", "https://t.me/graceboydeposit/3"))
        self.RESULTS_CHANNEL_LINK: str = bot_config.get("results_channel_link", os.getenv("RESULTS_CHANNEL_LINK", "https://t.me/Graceboytrading"))
        self.SUPPORT_USERNAME: str = bot_config.get("support_username", os.getenv("SUPPORT_USERNAME", "graceboysupport"))
        self.DIRECT_CONTACT_USERNAME: str = bot_config.get("direct_contact_username", os.getenv("DIRECT_CONTACT_USERNAME", "graceboylive"))
        self.PROMO_CODE: str = bot_config.get("promo_code", os.getenv("PROMO_CODE", "GRACEBOY100"))
        
        # Timing Configuration
        self.FOLLOW_UP_1_MINUTES: int = timing_config.get("follow_up_1_minutes", int(os.getenv("FOLLOW_UP_1_MINUTES", "1")))
        self.FOLLOW_UP_3_MINUTES: int = timing_config.get("follow_up_3_minutes", int(os.getenv("FOLLOW_UP_3_MINUTES", "3")))
        
        # Custom Messages
        self.WELCOME_MESSAGE: str = messages_config.get("welcome_message", os.getenv("WELCOME_MESSAGE", """Welcome, {first_name}!

This is the exact system that changed my life entirely as well as thousands of others….same system I used to charge over $1k for — and now, I'm giving it to you for FREE.

automatic signal delivery straight from my private bot with over 90% WIN Accuracy

This opportunity won't stay FREE forever. Once access closes, IT'S DONE.

Click 👉 /start now to get FREE ACCESS IMMEDIATELY"""))
        
        self.IMMEDIATE_FOLLOW_UP: str = messages_config.get("immediate_follow_up", os.getenv("IMMEDIATE_FOLLOW_UP", """🔁 Immediate Follow-Up

Click 👉 /start now — get the bot plugged in and start catching real-time trades.

Access is limited. Don't be the one watching from outside."""))
        
        self.SETUP_INSTRUCTIONS: str = messages_config.get("setup_instructions", os.getenv("SETUP_INSTRUCTIONS", """🔥 You made it in, {first_name}!

Let's plug you into the system properly:

You know you need a Trading account to Access my Bot right?? You need to be ready 

Creating your trading account isn't hard, but I have provided you a detailed step by Step Guide to achieve that below 👇

{deposit_guide_link}

Only serious ones get access, so a minimum of $20 deposit on your personal trading would grant you FREE Access

Infact, you can join my public telegram I opened recently where I share RESULTS 👇

{results_channel_link}"""))
        
        self.SUPPORT_MESSAGE: str = messages_config.get("support_message", os.getenv("SUPPORT_MESSAGE", """📍 Immediate Message

Send a screenshot of your account + deposit proof to my support team 👉 @{support_username}

Once they verify, the signal bot will be activated immediately and start delivering trades to you 24/7.

This is a one-time setup.

After this, you're officially in."""))
        
        self.FOLLOW_UP_1H: str = messages_config.get("follow_up_1h", os.getenv("FOLLOW_UP_1H", """🕐 First Follow-Up

Hey 👋

Just checking in — have you created your account and sent proof to support yet?"""))
        
        self.FOLLOW_UP_3H: str = messages_config.get("follow_up_3h", os.getenv("FOLLOW_UP_3H", """🕒 Final Follow-Up

Hey again, {first_name}!

Just checking one last time.

If you got stuck or have questions, reach out to me directly here @{direct_contact_username}

Let's not waste time — this bot is literally printing results every day.

You either plug in or watch others eat.

You need the Step by step guide to setting up your account? Here 👇

{deposit_guide_link}"""))
        
        self.SETUP_COMPLETED_MSG: str = messages_config.get("setup_completed_msg", os.getenv("SETUP_COMPLETED_MSG", """Perfect.

You're officially inside. Stay locked in — signals are already flowing, and we're entering new trades soon.

You're good now.

Just follow what the bot tells you."""))
        
        self.SETUP_REMINDER_MSG: str = messages_config.get("setup_reminder_msg", os.getenv("SETUP_REMINDER_MSG", """Let's wrap it up right now ✅

Here's the Step by Step setup guide to creating your trading account to get you ready👇

👉 {deposit_guide_link}

Don't forget the promo code: {promo_code} for up to 150% bonus.

After funding, send proof to @{support_username} so we activate the bot for you."""))
    
    def validate(self):
        """Validate that all required environment variables are set"""
        errors = []
        
        if not self.API_ID or self.API_ID == 0:
            errors.append("API_ID is required")
        
        if not self.API_HASH:
            errors.append("API_HASH is required")
        
        if not self.BOT_TOKEN:
            errors.append("BOT_TOKEN is required")
        
        if not self.CHID or self.CHID == 0:
            errors.append("CHID is required")
        
        if not self.SUDO:
            errors.append("SUDO is required")
        
        if not self.MONGO_URI:
            errors.append("MONGO_URI is required")
        
        if errors:
            raise ValueError(f"Missing required environment variables: {', '.join(errors)}")
        
        return True

# Create and validate configuration
cfg = Config()
cfg.validate()


