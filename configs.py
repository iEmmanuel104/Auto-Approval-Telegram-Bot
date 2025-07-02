from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", ""))
    API_HASH = getenv("API_HASH", "")
    BOT_TOKEN = getenv("BOT_TOKEN", "")
    # Your Force Subscribe Channel Id Below 
    CHID = int(getenv("CHID", "")) # Make Bot Admin In This Channel
    # Admin Or Owner Id Below
    SUDO = list(map(int, getenv("SUDO", "").split()))
    MONGO_URI = getenv("MONGO_URI", "")
    # Channel and Support URLs
    CHANNEL_URL = getenv("CHANNEL_URL", "https://t.me/AutoBot")
    SUPPORT_URL = getenv("SUPPORT_URL", "https://t.me/AutoBot")
    
cfg = Config()


