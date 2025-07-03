import os
import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from handlers.start import start_handler  # ✅ start handler import
from bot_data import USERS, GROUPS

BOT_TOKEN = os.getenv("BOT_TOKEN")  # ✅ Set in Replit Secrets

# 🔗 Link Regex
LINK_REGEX = r"(t\.me\/|https:\/\/t\.me\/|@[\w\d_]+)"

# 🔢 Track users and groups
USERS = set()
GROUPS = set()


# 🧹 Delete Telegram links from group messages
async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if message and re.search(LINK_REGEX, message.text):
        chat = update.effective_chat
        if chat.type in ["group", "supergroup"]:
            GROUPS.add(chat.id)  # 📌 Track group ID
        try:
            await message.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")


# 📊 /stats command handler
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USERS.add(
        update.effective_user.id)  # ✅ Ensure user is counted if using /stats
    text = f"📊 Bot Stats:\n\n👥 Users: {len(USERS)}\n👨‍👩‍👧‍👦 Groups: {len(GROUPS)}"
    await update.message.reply_text(text)


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("stats", stats_command))  # ✅ /stats added
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.ChatType.GROUPS & filters.Regex(LINK_REGEX),
            delete_links,
        ))

    print("🤖 Bot started.")
    app.run_polling()
