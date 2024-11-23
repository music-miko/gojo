import asyncio
import random
from sys import version_info

from pyrogram import __version__ as pver
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Curse import UPTIME
from Curse.bot_class import app
from Curse import PREFIX_HANDLER as COMMAND_HANDLER

StartPic = [
    "https://telegra.ph/file/0e1d42b86f4a167972839-844e0c51a92326ea40.jpg",
    "https://telegra.ph/file/7df2de352a15bb476687d-6028f1319812b91775.jpg",
    "https://telegra.ph/file/31caba1a922f23ea9b47c-ed6d092f5b11bb35a7.jpg",
    "https://telegra.ph/file/12a70be5ce2ef0390c283-6471cefed0a23c07af.jpg",
]

Suku = [
    [
        InlineKeyboardButton(text=" Sᴜᴘᴘᴏʀᴛ ", url="https://t.me/hunterxsupport"),
        InlineKeyboardButton(text=" Uᴘᴅᴀᴛᴇs ", url=f"https://t.me/the_hogwart"),
    ],
    [
        InlineKeyboardButton(
            text=" Aᴅᴅ Mᴇ Iɴ Yᴏᴜʀ Gʀᴏᴜᴘ 💫 ",
            url="https://t.me/Harry_RoxBot?startgroup=new",
        ),
    ],
]


@app.on_message(filters.command(["alive", "zinda ho"], COMMAND_HANDLER), group=4678)
async def restart(client, m: Message):
up = strftime("%Hh %Mm %Ss", gmtime(time() - UPTIME))
    await m.delete()
    await m.reply_photo(
        random.choice(StartPic),
        caption=f"""
✨ I'm Harry Potter
🍀 I'm Working Fine as always 

👑 My Creator: [Damian](t.me/about_tosu) 
🧑‍💻 My Devs : [Tosu](t.me/itz_tusarr) 

🧚‍♂️ Bot version: Harry Potter 2.8
🐍 Python-Telegram-Bot:21.6
⚡ Uptime: {up}""",
        reply_markup=InlineKeyboardMarkup(Suku),
    )
