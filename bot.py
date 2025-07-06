import logging
import asyncio
import random
import os
from datetime import datetime, timedelta
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant, FloodWait
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import pytz

from database import (
    add_user, add_group, all_users, all_groups, users, remove_user,
    add_onboarding_user, get_onboarding_user, update_onboarding_stage,
    mark_follow_up_sent, mark_setup_completed, mark_account_verified,
    get_users_for_follow_up, is_user_in_onboarding, already_onboarding
)
from configs import cfg

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Create unique session name for different environments
session_name = f"graceboy_bot_{os.getenv('RAILWAY_ENVIRONMENT', 'local')}_{hash(cfg.BOT_TOKEN) % 10000}"

# Initialize bot client
app = Client(
    session_name,
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

# Initialize scheduler
scheduler = AsyncIOScheduler()

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Onboarding Flow ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def send_welcome_message(user_id: int, first_name: str):
    """Send the initial welcome message"""
    welcome_text = cfg.WELCOME_MESSAGE.format(first_name=first_name)
    
    try:
        await app.send_message(user_id, welcome_text)
        logger.info(f"Welcome message sent to user {user_id}")
    except Exception as e:
        logger.error(f"Error sending welcome message to {user_id}: {e}")

async def send_immediate_follow_up(user_id: int):
    """Send immediate follow-up message"""
    follow_up_text = cfg.IMMEDIATE_FOLLOW_UP
    
    try:
        await app.send_message(user_id, follow_up_text)
        logger.info(f"Immediate follow-up sent to user {user_id}")
    except Exception as e:
        logger.error(f"Error sending immediate follow-up to {user_id}: {e}")

async def send_setup_instructions(user_id: int, first_name: str):
    """Send setup instructions after /start command"""
    setup_text = cfg.SETUP_INSTRUCTIONS.format(
        first_name=first_name,
        deposit_guide_link=cfg.DEPOSIT_GUIDE_LINK,
        results_channel_link=cfg.RESULTS_CHANNEL_LINK
    )
    
    try:
        await app.send_message(user_id, setup_text)
        logger.info(f"Setup instructions sent to user {user_id}")
    except Exception as e:
        logger.error(f"Error sending setup instructions to {user_id}: {e}")

async def send_support_message(user_id: int):
    """Send support message"""
    support_text = cfg.SUPPORT_MESSAGE.format(support_username=cfg.SUPPORT_USERNAME)
    
    try:
        await app.send_message(user_id, support_text)
        logger.info(f"Support message sent to user {user_id}")
    except Exception as e:
        logger.error(f"Error sending support message to {user_id}: {e}")

async def send_1hour_follow_up(user_id: int):
    """Send 1-hour follow-up with Yes/No buttons"""
    follow_up_text = cfg.FOLLOW_UP_1H
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Yes, I have", callback_data="setup_yes"),
            InlineKeyboardButton("❌ No, not yet", callback_data="setup_no")
        ]
    ])
    
    try:
        await app.send_message(user_id, follow_up_text, reply_markup=keyboard)
        mark_follow_up_sent(user_id, "1h")
        logger.info(f"1-hour follow-up sent to user {user_id}")
    except Exception as e:
        logger.error(f"Error sending 1-hour follow-up to {user_id}: {e}")

async def send_3hour_follow_up(user_id: int, first_name: str):
    """Send 3-hour follow-up"""
    follow_up_text = cfg.FOLLOW_UP_3H.format(
        first_name=first_name,
        direct_contact_username=cfg.DIRECT_CONTACT_USERNAME,
        deposit_guide_link=cfg.DEPOSIT_GUIDE_LINK
    )
    
    try:
        await app.send_message(user_id, follow_up_text)
        mark_follow_up_sent(user_id, "3h")
        logger.info(f"3-hour follow-up sent to user {user_id}")
    except Exception as e:
        logger.error(f"Error sending 3-hour follow-up to {user_id}: {e}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Scheduler Functions ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def process_follow_ups():
    """Process scheduled follow-ups"""
    try:
        # Process 1-hour follow-ups
        users_1h = get_users_for_follow_up("1h", 1)
        for user in users_1h:
            await send_1hour_follow_up(int(user["user_id"]))
        
        # Process 3-hour follow-ups
        users_3h = get_users_for_follow_up("3h", 3)
        for user in users_3h:
            await send_3hour_follow_up(int(user["user_id"]), user["first_name"])
            
    except Exception as e:
        logger.error(f"Error processing follow-ups: {e}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel)
async def approve(_, m: Message):
    """Auto-approve chat join requests"""
    op = m.chat
    kk = m.from_user
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(op.id, kk.id)
        
        add_user(kk.id)
        logger.info(f"Approved join request for user {kk.id} in chat {op.id}")
        
    except errors.PeerIdInvalid:
        logger.warning(f"User {kk.id} hasn't started the bot")
    except Exception as err:
        logger.error(f"Error approving join request: {str(err)}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ New User Detection ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.private & filters.incoming)
async def handle_new_user(_, m: Message):
    """Handle new users and trigger onboarding"""
    user_id = m.from_user.id
    first_name = m.from_user.first_name or "Friend"
    
    # Skip if it's a command or user is already in onboarding
    if m.text and m.text.startswith('/'):
        return
    
    if not already_onboarding(user_id):
        # New user - start onboarding
        add_onboarding_user(user_id, first_name)
        add_user(user_id)
        
        # Send welcome message
        await send_welcome_message(user_id, first_name)
        
        # Send immediate follow-up after a short delay
        await asyncio.sleep(2)
        await send_immediate_follow_up(user_id)
        
        logger.info(f"Started onboarding for new user {user_id}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start Command ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.private & filters.command("start"))
async def start_command(_, m: Message):
    """Handle /start command"""
    user_id = m.from_user.id
    first_name = m.from_user.first_name or "Friend"
    
    # Check if user is member of required channel
    try:
        await app.get_chat_member(cfg.CHID, user_id)
    except:
        try:
            invite_link = await app.create_chat_invite_link(int(cfg.CHID))
        except Exception as e:
            logger.error(f"Error creating invite link: {str(e)}")
            await m.reply("**Make Sure I Am Admin In Your Channel**")
            return
        
        key = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🍿 Join Update Channel 🍿", url=invite_link.invite_link),
                InlineKeyboardButton("🍀 Check Again 🍀", callback_data="chk")
            ]
        ])
        
        await m.reply_text(
            "**⚠️ Access Denied! ⚠️\n\n"
            "Please Join My Update Channel To Use Me. "
            "If You Joined The Channel Then Click On Check Again Button To Confirm.**",
            reply_markup=key
        )
        return
    
    # User is authorized - check if they're in onboarding
    if not already_onboarding(user_id):
        # New user - start onboarding
        add_onboarding_user(user_id, first_name)
        add_user(user_id)
        
        # Send welcome message first
        await send_welcome_message(user_id, first_name)
        await asyncio.sleep(2)
        await send_immediate_follow_up(user_id)
    
    # Send setup instructions
    await send_setup_instructions(user_id, first_name)
    
    # Send support message
    await asyncio.sleep(2)
    await send_support_message(user_id)
    
    # Update onboarding stage
    update_onboarding_stage(user_id, "start_clicked")
    
    logger.info(f"User {user_id} clicked /start")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Callback Handlers ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def check_subscription(_, cb: CallbackQuery):
    """Handle check subscription callback"""
    user_id = cb.from_user.id
    first_name = cb.from_user.first_name or "Friend"
    
    try:
        await app.get_chat_member(cfg.CHID, user_id)
    except:
        await cb.answer(
            "🙅‍♂️ You are not joined my channel first join channel then check again. 🙅‍♂️",
            show_alert=True
        )
        return
    
    # User verified - check if they're in onboarding
    if not already_onboarding(user_id):
        # New user - start onboarding
        add_onboarding_user(user_id, first_name)
        add_user(user_id)
        
        # Send welcome message
        await send_welcome_message(user_id, first_name)
        await asyncio.sleep(2)
        await send_immediate_follow_up(user_id)
    
    # Send setup instructions
    await send_setup_instructions(user_id, first_name)
    
    # Send support message
    await asyncio.sleep(2)
    await send_support_message(user_id)
    
    # Update onboarding stage
    update_onboarding_stage(user_id, "verified")
    
    await cb.edit_message_text("✅ Welcome! Check your messages for setup instructions.")
    logger.info(f"User {user_id} verified subscription")

@app.on_callback_query(filters.regex("setup_yes"))
async def setup_yes_callback(_, cb: CallbackQuery):
    """Handle 'Yes, I have' callback"""
    user_id = cb.from_user.id
    
    response_text = cfg.SETUP_COMPLETED_MSG
    
    await cb.edit_message_text(response_text)
    
    # Mark as completed
    mark_setup_completed(user_id, True)
    mark_account_verified(user_id, True)
    update_onboarding_stage(user_id, "completed")
    
    logger.info(f"User {user_id} confirmed setup completion")

@app.on_callback_query(filters.regex("setup_no"))
async def setup_no_callback(_, cb: CallbackQuery):
    """Handle 'No, not yet' callback"""
    user_id = cb.from_user.id
    
    response_text = cfg.SETUP_REMINDER_MSG.format(
        deposit_guide_link=cfg.DEPOSIT_GUIDE_LINK,
        promo_code=cfg.PROMO_CODE,
        support_username=cfg.SUPPORT_USERNAME
    )
    
    await cb.edit_message_text(response_text)
    
    # Update stage but don't mark as completed
    update_onboarding_stage(user_id, "setup_reminder_sent")
    
    logger.info(f"User {user_id} needs setup reminder")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Admin Commands ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def get_stats(_, m: Message):
    """Get bot statistics (admin only)"""
    try:
        xx = all_users()
        x = all_groups()
        tot = int(xx + x)
        
        stats_text = f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users : `{xx}`
👥 Groups : `{x}`
🚧 Total users & groups : `{tot}`
        """
        
        await m.reply_text(text=stats_text)
        logger.info(f"Stats requested by admin {m.from_user.id}")
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        await m.reply_text("Error getting statistics.")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def broadcast(_, m: Message):
    """Broadcast message to all users (admin only)"""
    if not m.reply_to_message:
        await m.reply_text("Please reply to a message to broadcast.")
        return
    
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            await m.reply_to_message.copy(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            logger.error(f"Broadcast error: {str(e)}")
            failed += 1
    
    result_text = (
        f"✅ Successfully sent to `{success}` users.\n"
        f"❌ Failed to send to `{failed}` users.\n"
        f"👾 Found `{blocked}` blocked users\n"
        f"👻 Found `{deactivated}` deactivated users."
    )
    
    await lel.edit(result_text)
    logger.info(f"Broadcast completed by admin {m.from_user.id}: {success} successful, {failed} failed")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def forward_broadcast(_, m: Message):
    """Forward message to all users (admin only)"""
    if not m.reply_to_message:
        await m.reply_text("Please reply to a message to forward.")
        return
    
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            await m.reply_to_message.forward(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            logger.error(f"Forward broadcast error: {str(e)}")
            failed += 1
    
    result_text = (
        f"✅ Successfully sent to `{success}` users.\n"
        f"❌ Failed to send to `{failed}` users.\n"
        f"👾 Found `{blocked}` blocked users\n"
        f"👻 Found `{deactivated}` deactivated users."
    )
    
    await lel.edit(result_text)
    logger.info(f"Forward broadcast completed by admin {m.from_user.id}: {success} successful, {failed} failed")

# Start the bot
if __name__ == "__main__":
    logger.info(f"Starting {cfg.BOT_NAME}...")
    print(f"🤖 {cfg.BOT_NAME} is starting...")
    
    try:
        # Start scheduler
        scheduler.add_job(
            process_follow_ups,
            IntervalTrigger(minutes=10),  # Check every 10 minutes
            id='follow_up_processor',
            replace_existing=True
        )
        scheduler.start()
        logger.info("Scheduler started")
        
        # Start bot
        app.run()
    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}")
        print(f"❌ Error starting bot: {str(e)}")
    finally:
        scheduler.shutdown()
        logger.info("Bot stopped.")
        print("🛑 Bot stopped.")
