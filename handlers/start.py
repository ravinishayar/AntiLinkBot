from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("➕ Add me to your group",
                             url="https://t.me/LinksDeleteBot?startgroup=true")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "I'm a powerful Anti-Link Bot designed to keep your Telegram groups safe. 🚫\n\n"
        "🔹 I automatically delete any Telegram invite links, usernames, or spam links.\n"
        "🔹 Just add me to your group and make me admin.\n\n"
        "Let me help you keep your group clean and spam-free! 💪",
        reply_markup=reply_markup)
