from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot_data import save_group


async def welcome_on_group_add(update: Update,
                               context: ContextTypes.DEFAULT_TYPE):
    # ✅ Check if bot was added to the group
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            chat_id = update.effective_chat.id

            # ✅ Save group in MongoDB
            save_group(chat_id)

            # 💬 Welcome Message
            welcome_text = (
                "👋 **Thanks for adding me!**\n\n"
                "✨ ɪ'ᴍ ᴀɴ ᴀɴᴛɪ-ʟɪɴᴋ ʙᴏᴛ 🚫\n"
                "🔹 I will automatically delete Telegram invite links, usernames, and spam links.\n\n"
                "👑 **Promote me to Admin** to activate full protection.\n"
                "Let's keep this group clean and safe! ✅")

            # 📎 Inline Buttons
            buttons = [[
                InlineKeyboardButton("👑 Owner",
                                     url="https://t.me/ravinishayar54"),
                InlineKeyboardButton("💬 Support",
                                     url="https://t.me/GroupHelpChatGuard")
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)

            # ✅ Send welcome message in the group
            await update.message.reply_text(text=welcome_text,
                                            reply_markup=reply_markup,
                                            parse_mode="Markdown")
