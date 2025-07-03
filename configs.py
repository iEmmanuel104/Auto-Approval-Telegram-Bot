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
    CHANNEL_URL: str = os.getenv("CHANNEL_URL", "https://t.me/AutoBot")
    SUPPORT_URL: str = os.getenv("SUPPORT_URL", "https://t.me/AutoBot")
    
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


