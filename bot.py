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
    get_users_for_follow_up, is_user_in_onboarding, already_onboarding,
    reset_onboarding
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
    bot_token=cfg.BOT_TOKEN,
    workers=50,  # Increased workers for high concurrency
    sleep_threshold=180  # Longer sleep threshold for flood wait
)

# Initialize scheduler
scheduler = AsyncIOScheduler()

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Debug Handler (Priority) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("test") & filters.private)
async def test_admin_priority(_, m: Message):
    """Test admin permissions and message functionality"""
    user_id = m.from_user.id
    first_name = m.from_user.first_name or "Friend"
    
    logger.info(f"🔍 PRIORITY: /test command from user {user_id}")
    logger.info(f"🔍 PRIORITY: cfg.SUDO contains: {cfg.SUDO}")
    logger.info(f"🔍 PRIORITY: Is {user_id} in SUDO? {user_id in cfg.SUDO}")
    
    try:
        if user_id in cfg.SUDO:
            await m.reply_text(f"✅ You are an admin! Your ID: {user_id}")
            
            # Test welcome message functionality
            try:
                logger.info(f"🔍 DEBUG: Testing welcome message for admin {user_id}")
                await send_welcome_message(user_id, first_name)
                await m.reply_text("✅ Welcome message test: SUCCESS")
            except Exception as e:
                logger.error(f"🔍 DEBUG: Welcome message test failed: {e}")
                await m.reply_text(f"❌ Welcome message test: FAILED - {e}")
                
        else:
            await m.reply_text(f"❌ You are not an admin. Your ID: {user_id}\nAdmin IDs: {cfg.SUDO}")
            
            # Test welcome message for regular user
            try:
                logger.info(f"🔍 DEBUG: Testing welcome message for user {user_id}")
                await send_welcome_message(user_id, first_name)
                await m.reply_text("✅ Welcome message test: SUCCESS")
            except Exception as e:
                logger.error(f"🔍 DEBUG: Welcome message test failed: {e}")
                await m.reply_text(f"❌ Welcome message test: FAILED - {e}")
                
    except Exception as e:
        logger.error(f"Error in test command: {e}")
        await m.reply_text(f"Error: {e}")

@app.on_message(filters.command("resetonboarding") & filters.user(cfg.SUDO))
async def reset_onboarding_command(_, m: Message):
    """Reset onboarding for a user (admin only)"""
    user_id = m.from_user.id
    
    try:
        # Check if there's a user ID in the command
        parts = m.text.split()
        if len(parts) > 1:
            target_user_id = int(parts[1])
        else:
            target_user_id = user_id
            
        if already_onboarding(target_user_id):
            reset_onboarding(target_user_id)
            await m.reply_text(f"✅ Reset onboarding for user {target_user_id}")
            logger.info(f"Admin {user_id} reset onboarding for user {target_user_id}")
        else:
            await m.reply_text(f"❌ User {target_user_id} has no onboarding record")
            
    except ValueError:
        await m.reply_text("❌ Invalid user ID. Usage: /resetonboarding [user_id]")
    except Exception as e:
        logger.error(f"Error in reset onboarding command: {e}")
        await m.reply_text(f"Error: {e}")

@app.on_message(filters.command("testbuttons") & filters.user(cfg.SUDO))
async def test_buttons_command(_, m: Message):
    """Test button functionality (admin only)"""
    user_id = m.from_user.id
    
    try:
        # Create test buttons
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Test Yes", callback_data="setup_yes"),
                InlineKeyboardButton("❌ Test No", callback_data="setup_no")
            ],
            [
                InlineKeyboardButton("🔄 Test Check", callback_data="chk")
            ]
        ])
        
        test_message = """
🧪 **Button Test for Admin**

Click the buttons below to test the callback functionality:

• **Test Yes** - Should show setup completion message
• **Test No** - Should show setup reminder message  
• **Test Check** - Should test subscription verification

This is for debugging purposes only.
        """
        
        await m.reply_text(test_message, reply_markup=keyboard)
        logger.info(f"Admin {user_id} initiated button test")
        
    except Exception as e:
        logger.error(f"Error in test buttons command: {e}")
        await m.reply_text(f"Error: {e}")

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
        results_channel_link=cfg.RESULTS_CHANNEL_LINK,
        support_username=cfg.SUPPORT_USERNAME
    )
    
    try:
        await app.send_message(user_id, setup_text)
        logger.info(f"Setup instructions sent to user {user_id}")
    except Exception as e:
        logger.error(f"Error sending setup instructions to {user_id}: {e}")

async def send_support_message(user_id: int):
    """Send support message"""
    support_text = cfg.SUPPORT_MESSAGE.format(
        support_username=cfg.SUPPORT_USERNAME,
        deposit_guide_link=cfg.DEPOSIT_GUIDE_LINK,
        results_channel_link=cfg.RESULTS_CHANNEL_LINK
    )
    
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
        # Process 1-minute follow-ups (configurable)
        users_1m = get_users_for_follow_up("1h", cfg.FOLLOW_UP_1_MINUTES)
        for user in users_1m:
            await send_1hour_follow_up(int(user["user_id"]))
        
        # Process 3-minute follow-ups (configurable)
        users_3m = get_users_for_follow_up("3h", cfg.FOLLOW_UP_3_MINUTES)
        for user in users_3m:
            await send_3hour_follow_up(int(user["user_id"]), user["first_name"])
            
    except Exception as e:
        logger.error(f"Error processing follow-ups: {e}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel)
async def approve(_, m: Message):
    """Auto-approve chat join requests and start onboarding flow"""
    op = m.chat
    kk = m.from_user
    logger.info(f"🔍 DEBUG: Join request received from user {kk.id} ({kk.first_name}) in chat {op.id} ({op.title})")
    
    try:
        add_group(m.chat.id)
        logger.info(f"🔍 DEBUG: Added group {op.id} to database")
        
        await app.approve_chat_join_request(op.id, kk.id)
        logger.info(f"🔍 DEBUG: Approved join request for user {kk.id}")
        
        add_user(kk.id)
        logger.info(f"🔍 DEBUG: Added user {kk.id} to database")
        
        # Start onboarding flow for new users (skip if admin)
        user_id = kk.id
        first_name = kk.first_name or "Friend"
        
        # Skip onboarding for admins
        if user_id in cfg.SUDO:
            logger.info(f"🔍 DEBUG: Skipping onboarding for admin user {user_id}")
            logger.info(f"Approved join request for admin user {kk.id} in chat {op.id}")
            return
        
        logger.info(f"🔍 DEBUG: Starting onboarding process for user {user_id}")
        
        # Always reset onboarding for fresh start (handles rejoin scenarios)
        if already_onboarding(user_id):
            logger.info(f"🔍 DEBUG: User {user_id} has existing onboarding record - resetting for fresh start")
            # Remove existing onboarding record
            reset_onboarding(user_id)
            logger.info(f"🔍 DEBUG: Removed existing onboarding record for user {user_id}")
        
        # Create fresh onboarding record for all users
        logger.info(f"🔍 DEBUG: Creating fresh onboarding record for user {user_id}")
        add_onboarding_user(user_id, first_name)
        logger.info(f"🔍 DEBUG: Added user {user_id} to onboarding database")
        
        # Always try to send welcome message on approval
        try:
            logger.info(f"🔍 DEBUG: Attempting to send welcome message to user {user_id}")
            await send_welcome_message(user_id, first_name)
            logger.info(f"🔍 DEBUG: Welcome message sent successfully to user {user_id}")
            
            # Send immediate follow-up after a short delay
            await asyncio.sleep(2)
            logger.info(f"🔍 DEBUG: Sending immediate follow-up to user {user_id}")
            await send_immediate_follow_up(user_id)
            logger.info(f"🔍 DEBUG: Immediate follow-up sent to user {user_id}")
            
            # Update stage to indicate welcome was sent
            update_onboarding_stage(user_id, "welcome_actually_sent")
            logger.info(f"🔍 DEBUG: Updated onboarding stage for user {user_id} to 'welcome_actually_sent'")
            logger.info(f"Started onboarding for user {user_id} after auto-approval")
            
        except errors.PeerIdInvalid:
            logger.warning(f"🔍 DEBUG: PeerIdInvalid - User {user_id} hasn't started the bot - will send welcome when they message us")
            logger.info(f"🔍 DEBUG: Onboarding stage remains 'welcome_sent' (will send when user messages us)")
        except Exception as e:
            logger.error(f"🔍 DEBUG: Error sending welcome message to {user_id}: {e}")
            logger.exception("Full exception details:")
        
        logger.info(f"🔍 DEBUG: Approval process completed for user {kk.id} in chat {op.id}")
        
    except Exception as err:
        logger.error(f"🔍 DEBUG: Error in approval process: {str(err)}")
        logger.exception("Full exception details:")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ New User Detection ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.private & filters.incoming & ~filters.command(["start", "users", "bcast", "fcast", "test"]))
async def handle_new_user(_, m: Message):
    """Handle new users and trigger onboarding"""
    user_id = m.from_user.id
    first_name = m.from_user.first_name or "Friend"
    
    # Skip if it's a command (additional safety check)
    if m.text and m.text.startswith('/'):
        logger.info(f"🔍 DEBUG: Skipping command in handle_new_user: {m.text}")
        return
    
    # Skip onboarding for admins
    if user_id in cfg.SUDO:
        logger.info(f"Skipping onboarding for admin user {user_id} in private message")
        return
    
    # Check if user is in onboarding
    if already_onboarding(user_id):
        user_data = get_onboarding_user(user_id)
        if user_data and user_data.get("onboarding_stage") == "welcome_sent":
            # User was auto-approved but welcome message wasn't sent due to PeerIdInvalid
            # Now they've messaged the bot, so we can send the onboarding flow
            await send_welcome_message(user_id, first_name)
            
            # Send immediate follow-up after a short delay
            await asyncio.sleep(2)
            await send_immediate_follow_up(user_id)
            
            # Update stage to indicate welcome was actually sent
            update_onboarding_stage(user_id, "welcome_actually_sent")
            logger.info(f"Sent delayed welcome message to user {user_id}")
        # If they already got welcome message, do nothing (avoid spam)
    else:
        # Completely new user who didn't come through channel approval
        add_onboarding_user(user_id, first_name)
        add_user(user_id)
        
        # Send welcome message
        await send_welcome_message(user_id, first_name)
        
        # Send immediate follow-up after a short delay
        await asyncio.sleep(2)
        await send_immediate_follow_up(user_id)
        
        # Update stage
        update_onboarding_stage(user_id, "welcome_actually_sent")
        logger.info(f"Started onboarding for new user {user_id}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start Command ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.private & filters.command("start"))
async def start_command(_, m: Message):
    """Handle /start command"""
    user_id = m.from_user.id
    first_name = m.from_user.first_name or "Friend"
    
    # Skip onboarding for admins
    if user_id in cfg.SUDO:
        await m.reply_text("👋 Welcome back, Admin!")
        logger.info(f"Admin {user_id} used /start command")
        return
    
    # Check if user is member of required channel
    try:
        print("🔍 DEBUG: User is member of required channel")
        # await send_setup_instructions(user_id, first_name)
        # await app.get_chat_member(cfg.CHID, user_id)
    except:
        try:
            invite_link = await app.create_chat_invite_link(int(cfg.CHID))
        except Exception as e:
            logger.error(f"Error creating invite link: {str(e)}")
            # await m.reply("**Make Sure I Am Admin In Your Channel**")
            await m.reply("**Welcome**")
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
    
    # User is authorized - check onboarding status
    if already_onboarding(user_id):
        user_data = get_onboarding_user(user_id)
        if user_data and user_data.get("onboarding_stage") == "welcome_sent":
            # User was auto-approved but welcome message wasn't sent yet
            # Send welcome message first
            await send_welcome_message(user_id, first_name)
            await asyncio.sleep(2)
            await send_immediate_follow_up(user_id)
            await asyncio.sleep(2)
    else:
        # Completely new user - start onboarding
        add_onboarding_user(user_id, first_name)
        add_user(user_id)
        
        # Send welcome message first
        await send_welcome_message(user_id, first_name)
        await asyncio.sleep(2)
        await send_immediate_follow_up(user_id)
        await asyncio.sleep(2)
    
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
    
    logger.info(f"🔍 DEBUG: User {user_id} clicked 'Check Again' button")
    
    try:
        await app.get_chat_member(cfg.CHID, user_id)
        logger.info(f"🔍 DEBUG: User {user_id} is verified as channel member")
    except Exception as e:
        logger.info(f"🔍 DEBUG: User {user_id} is not a channel member: {e}")
        await cb.answer(
            "🙅‍♂️ You are not joined my channel first join channel then check again. 🙅‍♂️",
            show_alert=True
        )
        return
    
    # Skip onboarding for admins
    if user_id in cfg.SUDO:
        await cb.edit_message_text("👋 Welcome back, Admin!")
        logger.info(f"Admin {user_id} verified subscription")
        return
    
    # User verified - check onboarding status
    if already_onboarding(user_id):
        user_data = get_onboarding_user(user_id)
        if user_data and user_data.get("onboarding_stage") == "welcome_sent":
            # User was auto-approved but welcome message wasn't sent yet
            # Send welcome message first
            await send_welcome_message(user_id, first_name)
            await asyncio.sleep(2)
            await send_immediate_follow_up(user_id)
            await asyncio.sleep(2)
    else:
        # Completely new user - start onboarding
        add_onboarding_user(user_id, first_name)
        add_user(user_id)
        
        # Send welcome message
        await send_welcome_message(user_id, first_name)
        await asyncio.sleep(2)
        await send_immediate_follow_up(user_id)
        await asyncio.sleep(2)
    
    # Send setup instructions
    await send_setup_instructions(user_id, first_name)
    
    # Send support message
    await asyncio.sleep(2)
    await send_support_message(user_id)
    
    # Update onboarding stage
    update_onboarding_stage(user_id, "verified")
    
    try:
        await cb.edit_message_text("✅ Welcome! Check your messages for setup instructions.")
        logger.info(f"🔍 DEBUG: Successfully edited subscription verification message for user {user_id}")
    except Exception as e:
        logger.error(f"🔍 DEBUG: Error editing subscription verification message for user {user_id}: {e}")
        # Try to answer callback if editing failed
        try:
            await cb.answer("✅ Welcome! Check your private messages for setup instructions.", show_alert=True)
        except:
            pass
    
    logger.info(f"User {user_id} verified subscription")

@app.on_callback_query(filters.regex("setup_yes"))
async def setup_yes_callback(_, cb: CallbackQuery):
    """Handle 'Yes, I have' callback"""
    user_id = cb.from_user.id
    
    try:
        logger.info(f"🔍 DEBUG: User {user_id} clicked 'Yes, I have' button")
        
        response_text = cfg.SETUP_COMPLETED_MSG
        
        # Try to edit the message
        await cb.edit_message_text(response_text)
        logger.info(f"🔍 DEBUG: Successfully edited message for user {user_id}")
        
        # Mark as completed
        mark_setup_completed(user_id, True)
        mark_account_verified(user_id, True)
        update_onboarding_stage(user_id, "completed")
        
        logger.info(f"User {user_id} confirmed setup completion")
        
        # Send confirmation callback answer
        await cb.answer("✅ Great! Setup completed successfully!", show_alert=False)
        
    except Exception as e:
        logger.error(f"🔍 DEBUG: Error in setup_yes_callback for user {user_id}: {e}")
        logger.exception("Full exception details:")
        # Try to answer the callback even if editing failed
        try:
            await cb.answer("❌ Error processing your response. Please try again.", show_alert=True)
        except:
            pass

@app.on_callback_query(filters.regex("setup_no"))
async def setup_no_callback(_, cb: CallbackQuery):
    """Handle 'No, not yet' callback"""
    user_id = cb.from_user.id
    
    try:
        logger.info(f"🔍 DEBUG: User {user_id} clicked 'No, not yet' button")
        
        response_text = cfg.SETUP_REMINDER_MSG.format(
            deposit_guide_link=cfg.DEPOSIT_GUIDE_LINK,
            promo_code=cfg.PROMO_CODE,
            support_username=cfg.SUPPORT_USERNAME
        )
        
        # Try to edit the message
        await cb.edit_message_text(response_text)
        logger.info(f"🔍 DEBUG: Successfully edited message for user {user_id}")
        
        # Update stage but don't mark as completed
        update_onboarding_stage(user_id, "setup_reminder_sent")
        
        logger.info(f"User {user_id} needs setup reminder")
        
        # Send confirmation callback answer
        await cb.answer("📝 No problem! Here's a reminder to help you get started.", show_alert=False)
        
    except Exception as e:
        logger.error(f"🔍 DEBUG: Error in setup_no_callback for user {user_id}: {e}")
        logger.exception("Full exception details:")
        # Try to answer the callback even if editing failed
        try:
            await cb.answer("❌ Error processing your response. Please try again.", show_alert=True)
        except:
            pass

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Admin Commands ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━



@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def get_stats(_, m: Message):
    """Get bot statistics (admin only)"""
    try:
        logger.info(f"Stats command triggered by user {m.from_user.id}")
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
    logger.info(f"Broadcast command triggered by user {m.from_user.id}")
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
    logger.info(f"Forward broadcast command triggered by user {m.from_user.id}")
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
            IntervalTrigger(seconds=30),  # Check every 30 seconds for testing
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
