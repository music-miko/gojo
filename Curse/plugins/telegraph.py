# DONE: Telegraph

import os
import requests
import aiohttp
import aiofiles
from aiohttp import ContentTypeError
from datetime import datetime

from PIL import Image
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.types.bots_and_keyboards.inline_keyboard_button import InlineKeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import InlineKeyboardMarkup
from telegraph import Telegraph, exceptions, upload_file

from Curse.bot_class import app

from catbox import CatboxUploader


uploader = CatboxUploader()
TMP_DOWNLOAD_DIRECTORY = "catbox/"


@app.on_message(filters.command(["tgm", "tmg", "telegraph"], prefixes="/"), group=9990009)
async def _(client, message):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        start = datetime.now()
        r_message = await event.get_reply_message()
        downloaded_file_name = await client.download_media(
                r_message, TMP_DOWNLOAD_DIRECTORY
            )
        end = datetime.now()
        ms = (end - start).seconds
        h = await event.reply(
            f"Downloaded to {downloaded_file_name} in {ms} seconds."
        )
        if downloaded_file_name.endswith((".webp")):
            resize_image(downloaded_file_name)
        try:
            start = datetime.now()
            media_urls = uploader.upload_file(downloaded_file_name)
        except:
            os.remove(downloaded_file_name)
        else:                
            end = datetime.now()
            ms_two = (end - start).seconds
            os.remove(downloaded_file_name)
            await h.edit(
                f"Uploaded to [Catbox]({media_urls}) in {ms + ms_two} seconds.",
                link_preview=True,
            )       
    else:
        await event.reply("Reply to a message to get a permanent catbox link.")


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")




@app.on_message(filters.command("txt"), group=90990090)
async def txt(_, message):
  try:
    reply = message.reply_to_message

    if not reply or not reply.text:
        return await message.reply("Reply to a text message")

    if len(message.command) < 2:
        return await message.reply("Usage:\n /txt [Page name]")

    page_name = message.text.split(None, 1)[1]
    page = telegraph.create_page(
        page_name, html_content=(reply.text.html).replace("\n", "<br>")
    )
    return await message.reply(
        f"Posted: {page['url']}",reply_markup=InlineKeyboardMarkup([ 
        [InlineKeyboardButton('View 💫' , url=f"{page['url']}")]
    ]),disable_web_page_preview=True,
    )
  except Exception as e:
       await message.reply_text(f"ERROR: {e}")

def check_filename(filroid):
    if os.path.exists(filroid):
        no = 1
        while True:
            ult = "{0}_{2}{1}".format(*os.path.splitext(filroid) + (no,))
            if os.path.exists(ult):
                no += 1
            else:
                return ult
    return filroid

async def RemoveBG(input_file_name):
    headers = {"X-API-Key": "u4x2416NAQVefYsfwbzrw7VE"}
    files = {"image_file": open(input_file_name, "rb").read()}
    async with aiohttp.ClientSession() as ses:
        async with ses.post(
            "https://api.remove.bg/v1.0/removebg", headers=headers, data=files
        ) as y:
            contentType = y.headers.get("content-type")
            if "image" not in contentType:
                return False, (await y.json())

            name = check_filename("Komi.png")
            file = await aiofiles.open(name, "wb")
            await file.write(await y.read())
            await file.close()
            return True, name


@app.on_message(filters.command("rmbg"), group=90906)
async def rmbg(bot, message):
  rmbg = await message.reply("Processing...") 
  replied = message.reply_to_message
  if not replied:
      return await rmbg.edit("Reply to a photo to Remove it's Backgroud")

  if replied.photo:
      photo = await bot.download_media(replied)
      x, y = await RemoveBG(photo)
      os.remove(photo)
      if not x:
          bruh = y["errors"][0]
          details = bruh.get("detail", "")
          return await rmbg.edit(f"ERROR ~ {bruh['title']},\n{details}")
      await message.reply_photo(photo=y,caption="Here is your Image without Background")
      await message.reply_document(document=y)
      await rmbg.delete()
      return os.remove(y)
  await rmbg.edit("Reply only to a photo to Remove it's Background")


@app.on_message(filters.command("write"), group=12112)
async def handwrite(_, message: Message):
    if message.reply_to_message:
        text = message.reply_to_message.text
    else:
        text =message.text.split(None, 1)[1]
    m =await message.reply_text( "Please wait...,\n\nWriting your text...")
    write = requests.get(f"https://apis.xditya.me/write?text={text}").url

    caption = f"""
sᴜᴄᴇssғᴜʟʟʏ ᴡʀɪᴛᴛᴇɴ ᴛᴇxᴛ 💘
✨ ᴡʀɪᴛᴛᴇɴ ʙʏ : [ʜᴀʀʀʏメᴘᴏᴛᴛᴇʀ](https://t.me/harry_RoxBot)
🥀 ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : {message.from_user.mention}
"""
    await m.delete()
    await message.reply_photo(photo=write,caption=caption)

__PLUGIN__ = "Telegraph"
__HELP__ = """
** About Telegraph **.

**Usage:**

➥ /tgm, /tm: convert photo to telegraph 
➥ /txt: reply to text to make your own telegraph paragraph
➥ /write: write something on page
"""
