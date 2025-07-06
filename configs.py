import os
from typing import List

class Config:
    # Required environment variables
    API_ID: int = int(os.getenv("API_ID", "0"))
    API_HASH: str = os.getenv("API_HASH", "")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    
    # Force Subscribe Channel ID
    CHID: int = int(os.getenv("CHID", "0"))
    
    # Admin/Owner User IDs (can be comma-separated)
    SUDO: List[int] = []
    if os.getenv("SUDO"):
        SUDO = [int(x.strip()) for x in os.getenv("SUDO").split(",")]
    
    # Database Configuration
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    
    # Optional URLs
    CHANNEL_URL: str = os.getenv("CHANNEL_URL", "https://t.me/xxxx")
    SUPPORT_URL: str = os.getenv("SUPPORT_URL", "https://t.me/xxxx")
    
    # Bot Configuration
    BOT_NAME: str = os.getenv("BOT_NAME", "Graceboy Trading Bot")
    
    # Trading Links
    DEPOSIT_GUIDE_LINK: str = os.getenv("DEPOSIT_GUIDE_LINK", "https://t.me/graceboydeposit/3")
    RESULTS_CHANNEL_LINK: str = os.getenv("RESULTS_CHANNEL_LINK", "https://t.me/Graceboytrading")
    SUPPORT_USERNAME: str = os.getenv("SUPPORT_USERNAME", "graceboysupport")
    DIRECT_CONTACT_USERNAME: str = os.getenv("DIRECT_CONTACT_USERNAME", "graceboylive")
    PROMO_CODE: str = os.getenv("PROMO_CODE", "GRACEBOY100")
    
    # Custom Messages
    WELCOME_MESSAGE: str = os.getenv("WELCOME_MESSAGE", """Welcome, {first_name}!

This is the exact system that changed my life entirely as well as thousands of others….same system I used to charge over $1k for — and now, I'm giving it to you for FREE.

automatic signal delivery straight from my private bot with over 90% WIN Accuracy

This opportunity won't stay FREE forever. Once access closes, IT'S DONE.

Click 👉 /start now to get FREE ACCESS IMMEDIATELY""")
    
    IMMEDIATE_FOLLOW_UP: str = os.getenv("IMMEDIATE_FOLLOW_UP", """🔁 Immediate Follow-Up

Click 👉 /start now — get the bot plugged in and start catching real-time trades.

Access is limited. Don't be the one watching from outside.""")
    
    SETUP_INSTRUCTIONS: str = os.getenv("SETUP_INSTRUCTIONS", """🔥 You made it in, {first_name}!

Let's plug you into the system properly:

You know you need a Trading account to Access my Bot right?? You need to be ready 

Creating your trading account isn't hard, but I have provided you a detailed step by Step Guide to achieve that below 👇

{deposit_guide_link}

Only serious ones get access, so a minimum of $20 deposit on your personal trading would grant you FREE Access

Infact, you can join my public telegram I opened recently where I share RESULTS 👇

{results_channel_link}""")
    
    SUPPORT_MESSAGE: str = os.getenv("SUPPORT_MESSAGE", """📍 Immediate Message

Send a screenshot of your account + deposit proof to my support team 👉 @{support_username}

Once they verify, the signal bot will be activated immediately and start delivering trades to you 24/7.

This is a one-time setup.

After this, you're officially in.""")
    
    FOLLOW_UP_1H: str = os.getenv("FOLLOW_UP_1H", """🕐 1 Hour Follow-Up

Hey 👋

Just checking in — have you created your account and sent proof to support yet?""")
    
    FOLLOW_UP_3H: str = os.getenv("FOLLOW_UP_3H", """🕒 3 Hour Follow-Up

Hey again, {first_name}!

Just checking one last time.

If you got stuck or have questions, reach out to me directly here @{direct_contact_username}

Let's not waste time — this bot is literally printing results every day.

You either plug in or watch others eat.

You need the Step by step guide to setting up your account? Here 👇

{deposit_guide_link}""")
    
    SETUP_COMPLETED_MSG: str = os.getenv("SETUP_COMPLETED_MSG", """Perfect.

You're officially inside. Stay locked in — signals are already flowing, and we're entering new trades soon.

You're good now.

Just follow what the bot tells you.""")
    
    SETUP_REMINDER_MSG: str = os.getenv("SETUP_REMINDER_MSG", """Let's wrap it up right now ✅

Here's the Step by Step setup guide to creating your trading account to get you ready👇

👉 {deposit_guide_link}

Don't forget the promo code: {promo_code} for up to 150% bonus.

After funding, send proof to @{support_username} so we activate the bot for you.""")
    
    # Validation
    @classmethod
    def validate(cls):
        """Validate that all required environment variables are set"""
        errors = []
        
        if not cls.API_ID or cls.API_ID == 0:
            errors.append("API_ID is required")
        
        if not cls.API_HASH:
            errors.append("API_HASH is required")
        
        if not cls.BOT_TOKEN:
            errors.append("BOT_TOKEN is required")
        
        if not cls.CHID or cls.CHID == 0:
            errors.append("CHID is required")
        
        if not cls.SUDO:
            errors.append("SUDO is required")
        
        if not cls.MONGO_URI:
            errors.append("MONGO_URI is required")
        
        if errors:
            raise ValueError(f"Missing required environment variables: {', '.join(errors)}")
        
        return True

# Validate configuration on import
Config.validate()
cfg = Config()


