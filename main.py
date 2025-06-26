import os
import re
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler,
                          ContextTypes, filters)

from handlers.start import start_handler  # ✅ start handler import

BOT_TOKEN = os.getenv("BOT_TOKEN")  # ✅ Make sure it's set in Replit secrets

LINK_REGEX = r"(t\.me\/|https:\/\/t\.me\/|@[\w\d_]+)"


async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if message and re.search(LINK_REGEX, message.text):
        try:
            await message.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.ChatType.GROUPS & filters.Regex(LINK_REGEX),
            delete_links))

    print("🤖 Bot started.")
    app.run_polling()
