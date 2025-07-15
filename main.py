import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from handlers.start import start_handler
from handlers.group_add import welcome_on_group_add
from bot_data import save_user, save_group, get_total_stats

BOT_TOKEN = os.getenv("BOT_TOKEN")

# 🔗 Anti-Link Regex
LINK_REGEX = r"(t\.me\/|https:\/\/t\.me\/|@[\w\d_]+)"


# 🧹 Auto-delete Telegram links in group messages
async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if message and re.search(LINK_REGEX, message.text):
        chat_id = update.effective_chat.id
        save_group(chat_id)
        try:
            await message.delete()
            print(f"✅ Deleted link in {chat_id}")
        except Exception as e:
            print(f"❌ Error deleting message: {e}")


# 📊 /stats command handler
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)
    total_users, total_groups = get_total_stats()
    text = ("📊 **Bot Stats:**\n\n"
            f"👤 **Users:** `{total_users}`\n"
            f"👥 **Groups:** `{total_groups}`")
    await update.message.reply_text(text, parse_mode="Markdown")


# 🚀 /start command handler
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_handler(update, context)


# 👋 Welcome message when bot is added to group
async def group_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await welcome_on_group_add(update, context)


# ✅ Initialize Application
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("stats", stats_command))
app.add_handler(
    MessageHandler(
        filters.TEXT & filters.ChatType.GROUPS & filters.Regex(LINK_REGEX),
        delete_links))
app.add_handler(
    MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, group_added))

# 🟢 Start polling
print("🤖 Bot started (Polling mode)...")
app.run_polling()
