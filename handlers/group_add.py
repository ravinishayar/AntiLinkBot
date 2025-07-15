from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot_data import save_group


@Client.on_message(filters.group & filters.service)
async def welcome_on_group_add(client: Client, message: Message):
    # ✅ Check if this service message is about bot being added
    if message.new_chat_members:
        for member in message.new_chat_members:
            if member.id == client.me.id:  # Check if bot is the one being added
                chat_id = message.chat.id

                # ✅ Save group in MongoDB
                save_group(chat_id)

                # 💬 Welcome Message
                welcome_text = (
                    "👋 **Thanks for adding me!**\n\n"
                    "✨ I'ᴍ ᴀɴ ᴀɴᴛɪ-ʟɪɴᴋ ʙᴏᴛ 🚫\n"
                    "🔹 I will automatically delete Telegram invite links, usernames, and spam links.\n\n"
                    "👑 **Promote me to Admin** to activate full protection.\n"
                    "Let's keep this group clean and safe! ✅")

                # 📎 Inline Buttons
                buttons = InlineKeyboardMarkup([[
                    InlineKeyboardButton("👑 Owner",
                                         url="https://t.me/ravinishayar54"),
                    InlineKeyboardButton("💬 Support",
                                         url="https://t.me/GroupHelpChatGuard")
                ]])

                # ✅ Send welcome message in the group
                await message.reply_text(welcome_text, reply_markup=buttons)
