from platform import python_version as y

from pyrogram import __version__ as z
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Curse.bot_class import app 

C_HANDLER = ["/", "harry ", "harry ", "."]

@app.on_message(filters.command(["repo", "source"], C_HANDLER), group=9966)
async def repo(_, message):
    await message.reply_photo(
        photo="https://telegra.ph/file/0e1d42b86f4a167972839-844e0c51a92326ea40.jpg",
        caption=f"""✨ **ʜᴇʏ {message.from_user.mention},**
**ʀᴇᴘᴏ ᴏᴡɴᴇʀ  : [Harry Potter](https://t.me/harry_roxbot)**
**ᴘʏᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ :** `{y()}`
**ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀꜱɪᴏɴ :** `{z}`
**ʙᴏᴛ ᴠᴇʀꜱɪᴏɴ :** `3.0`
""",
        reply_markup=InlineKeyboardMarkup(
     [[InlineKeyboardButton("𝚂ᴏᴜʀᴄᴇ",url="https://github.com/Infamous-Hydra/YaeMiko")]]
        ),
    )
