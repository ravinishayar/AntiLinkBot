from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot_data import save_user  # ✅ MongoDB function


async def start_handler(client: Client, message: Message):
    user_id = message.from_user.id
    save_user(user_id)  # ✅ Save user in MongoDB

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("➕ Add me to your group",
                             url="https://t.me/LinksDeleteBot?startgroup=true")
    ]])

    await message.reply_text(
        "👋 ᴡᴇʟᴄᴏᴍᴇ!\n\n"
        "ɪ'ᴍ ᴀ ᴘᴏᴡᴇʀꜰᴜʟ ᴀɴᴛɪ-ʟɪɴᴋ ʙᴏᴛ ᴅᴇꜱɪɢɴᴇᴅ ᴛᴏ ᴋᴇᴇᴘ ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘꜱ ꜱᴀꜰᴇ. 🚫\n\n"
        "🔹 ɪ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇ ᴀɴʏ ᴛᴇʟᴇɢʀᴀᴍ ɪɴᴠɪᴛᴇ ʟɪɴᴋꜱ, ᴜꜱᴇʀɴᴀᴍᴇꜱ, ᴏʀ ꜱᴘᴀᴍ ʟɪɴᴋꜱ.\n"
        "🔹 ᴊᴜꜱᴛ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ.\n\n"
        "ʟᴇᴛ ᴍᴇ ʜᴇʟᴘ ʏᴏᴜ ᴋᴇᴇᴘ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄʟᴇᴀɴ ᴀɴᴅ ꜱᴘᴀᴍ-ꜰʀᴇᴇ! 💪",
        reply_markup=keyboard)
