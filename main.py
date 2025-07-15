import os
import re
from pyrogram import Client, filters
from pyrogram.types import Message

from handlers.group_add import welcome_on_group_add
from handlers.start import start_handler
from bot_data import save_user, save_group, get_total_stats

# 🔑 Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Set in Replit/Secrets
API_ID = int(os.getenv("API_ID"))  # Your API_ID
API_HASH = os.getenv("API_HASH")  # Your API_HASH

# 🔗 Link Regex for Anti-Link
LINK_REGEX = r"(t\.me\/|https:\/\/t\.me\/|@[\w\d_]+)"

# ✅ Initialize Pyrogram Client
app = Client("AntiLinkBot",
             bot_token=BOT_TOKEN,
             api_id=API_ID,
             api_hash=API_HASH)


# 🧹 Auto-delete Telegram links in group messages
@app.on_message(filters.text & filters.group & filters.regex(LINK_REGEX))
async def delete_links(client: Client, message: Message):
    chat_id = message.chat.id
    save_group(chat_id)  # ✅ Save group in MongoDB
    try:
        await message.delete()
        print(f"✅ Deleted link in {chat_id}")
    except Exception as e:
        print(f"❌ Error deleting message: {e}")


# 📊 /stats command handler (Private Chat only)
@app.on_message(filters.command("stats") & filters.private)
async def stats_command(client: Client, message: Message):
    user_id = message.from_user.id
    save_user(user_id)  # ✅ Save user in MongoDB
    total_users, total_groups = get_total_stats()

    text = ("📊 **Bot Stats:**\n\n"
            f"👤 **Users:** `{total_users}`\n"
            f"👥 **Groups:** `{total_groups}`")
    await message.reply_text(text, quote=True)


# 🚀 /start command handler (Private Chat only)
@app.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    await start_handler(client, message)


# 👋 Welcome message when bot is added to group
@app.on_message(filters.group & filters.service)
async def group_service_handler(client: Client, message: Message):
    await welcome_on_group_add(client, message)


# ✅ Run Bot
print("🤖 Bot started (Pyrogram)...")
app.run()
