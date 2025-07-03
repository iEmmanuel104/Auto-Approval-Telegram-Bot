import logging
import asyncio
import random
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant, FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
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

# Initialize bot client
app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel)
async def approve(_, m: Message):
    """Auto-approve chat join requests"""
    op = m.chat
    kk = m.from_user
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(op.id, kk.id)
        
        # Send welcome message
        welcome_msg = f"**Hello {m.from_user.mention}!\nWelcome To {m.chat.title}\n\n__Powered By : @AutoBot__**"
        await app.send_message(kk.id, welcome_msg)
        
        add_user(kk.id)
        logger.info(f"Approved join request for user {kk.id} in chat {op.id}")
        
    except errors.PeerIdInvalid:
        logger.warning(f"User {kk.id} hasn't started the bot")
    except Exception as err:
        logger.error(f"Error approving join request: {str(err)}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.private & filters.command("start"))
async def start_command(_, m: Message):
    """Handle /start command"""
    try:
        # Check if user is member of required channel
        await app.get_chat_member(cfg.CHID, m.from_user.id)
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
    
    # User is authorized
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🗯 Channel", url=cfg.CHANNEL_URL),
            InlineKeyboardButton("💬 Support", url=cfg.SUPPORT_URL)
        ]
    ])
    
    add_user(m.from_user.id)
    
    welcome_text = (
        f"**🦊 Hello {m.from_user.mention}!\n"
        f"I'm an auto approve [Admin Join Requests](https://t.me/telegram/153) Bot.\n"
        f"I can approve users in Groups/Channels. Add me to your chat and promote me to admin "
        f"with add members permission.\n\n"
        f"__Powered By : @AutoBot__**"
    )
    
    await m.reply_photo(
        "https://graph.org/file/d57d6f83abb6b8d0efb02.jpg",
        caption=welcome_text,
        reply_markup=keyboard
    )
    
    logger.info(f"User {m.from_user.id} started the bot")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def check_subscription(_, cb: CallbackQuery):
    """Handle check subscription callback"""
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
    except:
        await cb.answer(
            "🙅‍♂️ You are not joined my channel first join channel then check again. 🙅‍♂️",
            show_alert=True
        )
        return
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🗯 Channel", url=cfg.CHANNEL_URL),
            InlineKeyboardButton("💬 Support", url=cfg.SUPPORT_URL)
        ]
    ])
    
    add_user(cb.from_user.id)
    
    welcome_text = (
        f"**🦊 Hello {cb.from_user.mention}!\n"
        f"I'm an auto approve [Admin Join Requests](https://t.me/telegram/153) Bot.\n"
        f"I can approve users in Groups/Channels. Add me to your chat and promote me to admin "
        f"with add members permission.\n\n"
        f"__Powered By : @AutoBot__**"
    )
    
    await cb.edit_message_text(text=welcome_text, reply_markup=keyboard)
    logger.info(f"User {cb.from_user.id} verified subscription")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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
    logger.info("Starting Auto Approval Bot...")
    print("🤖 Auto Approval Bot is starting...")
    
    try:
        app.run()
    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}")
        print(f"❌ Error starting bot: {str(e)}")
    finally:
        logger.info("Bot stopped.")
        print("🛑 Bot stopped.")
