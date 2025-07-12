from pymongo import MongoClient
from configs import cfg
from datetime import datetime, timedelta
import pytz

client = MongoClient(cfg.MONGO_URI)

users = client[cfg.DB_NAME]['users']
groups = client[cfg.DB_NAME]['groups']
onboarding = client[cfg.DB_NAME]['onboarding']

def already_db(user_id):
        user = users.find_one({"user_id" : str(user_id)})
        if not user:
            return False
        return True

def already_dbg(chat_id):
        group = groups.find_one({"chat_id" : str(chat_id)})
        if not group:
            return False
        return True

def add_user(user_id):
    in_db = already_db(user_id)
    if in_db:
        return
    return users.insert_one({"user_id": str(user_id)}) 

def remove_user(user_id):
    in_db = already_db(user_id)
    if not in_db:
        return 
    return users.delete_one({"user_id": str(user_id)})
    
def add_group(chat_id):
    in_db = already_dbg(chat_id)
    if in_db:
        return
    return groups.insert_one({"chat_id": str(chat_id)})

def all_users():
    user = users.find({})
    usrs = len(list(user))
    return usrs

def all_groups():
    group = groups.find({})
    grps = len(list(group))
    return grps

# Onboarding functions
def add_onboarding_user(user_id, first_name):
    """Add user to onboarding tracking with their first name"""
    utc = pytz.UTC
    now = datetime.now(utc)
    
    return onboarding.insert_one({
        "user_id": str(user_id),
        "first_name": first_name,
        "onboarding_stage": "welcome_sent",
        "created_at": now,
        "follow_up_1h_sent": False,
        "follow_up_3h_sent": False,
        "setup_completed": False,
        "account_verified": False
    })

def get_onboarding_user(user_id):
    """Get onboarding data for a user"""
    return onboarding.find_one({"user_id": str(user_id)})

def update_onboarding_stage(user_id, stage):
    """Update user's onboarding stage"""
    return onboarding.update_one(
        {"user_id": str(user_id)},
        {"$set": {"onboarding_stage": stage}}
    )

def mark_follow_up_sent(user_id, follow_up_type):
    """Mark a follow-up as sent"""
    field = f"follow_up_{follow_up_type}_sent"
    return onboarding.update_one(
        {"user_id": str(user_id)},
        {"$set": {field: True}}
    )

def mark_setup_completed(user_id, completed=True):
    """Mark user's setup as completed"""
    return onboarding.update_one(
        {"user_id": str(user_id)},
        {"$set": {"setup_completed": completed}}
    )

def mark_account_verified(user_id, verified=True):
    """Mark user's account as verified"""
    return onboarding.update_one(
        {"user_id": str(user_id)},
        {"$set": {"account_verified": verified}}
    )

def get_users_for_follow_up(follow_up_type, minutes_ago):
    """Get users who need follow-up messages"""
    utc = pytz.UTC
    cutoff_time = datetime.now(utc) - timedelta(minutes=minutes_ago)
    
    field = f"follow_up_{follow_up_type}_sent"
    
    return onboarding.find({
        "created_at": {"$lte": cutoff_time},
        field: False,
        "setup_completed": False
    })

def is_user_in_onboarding(user_id):
    """Check if user is in onboarding process"""
    user = onboarding.find_one({"user_id": str(user_id)})
    return user is not None

def already_onboarding(user_id):
    """Check if user already has onboarding record"""
    return onboarding.find_one({"user_id": str(user_id)}) is not None

def reset_onboarding(user_id):
    """Reset onboarding for a user (delete existing record)"""
    return onboarding.delete_one({"user_id": str(user_id)})
