import datetime
from datetime import date, datetime, time
from random import choice
from traceback import format_exc

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import CallbackQuery
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message

from Curse import BDB_URI, LOGGER, TIME_ZONE
from Curse.bot_class import app
from Curse.database.chats_db import Chats

if BDB_URI:
    from Curse.plugins import bday_cinfo, bday_info

from Curse.utils.custom_filters import command
from Curse.utils.extras import birthday_wish


def give_date(date, form="%d/%m/%Y"):
    datee = datetime.strptime(date, form).date()
    return datee


@app.on_message(command("remember"))
async def remember_me(c: app, m: Message):
    if not BDB_URI:
        await m.reply_text("BDB_URI is not configured")
        return
    splited = m.text.split()
    if len(splited) == 1:
        await m.reply_text(
            "**USAGE**:\n/remember [username or user id or reply to user] [DOB]\nDOB should be in format of dd/mm/yyyy\nYear is optional it is not necessary to pass it"
        )
        return
    if len(splited) != 2 and m.reply_to_message:
        await m.reply_text(
            "**USAGE**:\n/remember [username or user id or reply to user] [DOB]\nDOB should be in format of dd/mm/yyyy\nYear is optional it is not necessary to pass it"
        )
        return
    DOB = splited[1] if len(splited) == 2 else splited[2]
    if len(splited) == 2 and m.reply_to_message:
        user = m.reply_to_message.from_user.id
    elif not m.reply_to_message:
        user = m.from_user.id
    else:
        try:
            u_id = int(splited[1])
        except ValueError:
            pass
        try:
            user = await c.get_users(u_id)
        except Exception:
            u_u = await c.resolve_peer(u_id)
            try:
                user = (await c.get_users(u_u.user_id)).id
            except KeyError:
                await m.reply_text("Unable to find the user")
                return
    DOB = DOB.split("/")
    if len(DOB) != 3 and len(DOB) != 2:
        await m.reply_text(
            "DOB should be in format of dd/mm/yyyy\nYear is optional it is not necessary to pass it"
        )
        return
    is_correct = False
    if len(DOB) == 3:
        is_correct = len(DOB[2]) == 4
    if len(DOB[0]) != 2 and len(DOB[1]) != 2 and not is_correct:
        await m.reply_text(
            "DOB should be in format of dd/mm/yyyy\nYear is optional it is not necessary to pass it"
        )
        return
    try:
        date = int(DOB[0])
        month = int(DOB[1])
        if is_correct:
            year = int(DOB[2])
            is_year = 1
        else:
            year = "1900"
            is_year = 0
        DOB = f"{str(date)}/{str(month)}/{str(year)}"
    except ValueError:
        await m.reply_text("DOB should be numbers only")
        return

    data = {"user_id": user, "dob": DOB, "is_year": is_year}
    try:
        result = bday_info.find_one({"user_id": user})
        if result:
            await m.reply_text("User is already in my database")
            return
    except Exception as e:
        await m.reply_text(f"Got an error\n{e}")
        LOGGER.error(e)
        LOGGER.error(format_exc())
        return
    try:
        bday_info.insert_one(data)
        await m.reply_text("Your birthday is now registered in my database")
    except Exception as e:
        await m.reply_text(f"Got an error\n{e}")
        LOGGER.error(e)
        LOGGER.error(format_exc())
        return


@app.on_message(command(["removebday", "rmbday"]))
async def who_are_you_again(c: app, m: Message):
    if not BDB_URI:
        await m.reply_text("BDB_URI is not configured")
        return
    user = m.from_user.id
    try:
        result = bday_info.find_one({"user_id": user})
        if not result:
            await m.reply_text("User is not in my database")
            return
        elif result:
            bday_info.delete_one({"user_id": user})
            await m.reply_text("Removed your birthday")
            return
    except Exception as e:
        await m.reply_text(f"Got an error\n{e}")
        return


@app.on_message(command(["nextbdays", "nbdays", "birthdays", "bdays"]))
async def who_is_next(c: app, m: Message):
    if not BDB_URI:
        await m.reply_text("BDB_URI is not configured")
        return
    blist = list(bday_info.find())
    if m.chat.type == ChatType.PRIVATE:
        await m.reply_text("Use it in a group")
        return
    curr = datetime.now(TIME_ZONE).date()
    xx = await m.reply_text("📆")
    users = []
    today_users = []  # Users with birthday today

    if blist:
        for i in blist:
            if Chats(m.chat.id).user_is_in_chat(i["user_id"]):
                dob = give_date(i["dob"])
                if dob.month >= curr.month:
                    if (
                        dob.month == curr.month and not dob.day < curr.day
                    ) or dob.month >= curr.month:
                        if dob.month == curr.month and dob.day == curr.day:
                            today_users.append(i)  # Add to today's users list
                        else:
                            users.append(i)
                elif dob.month < curr.month:
                    pass
            if len(users) == 10:
                break

    if not users and not today_users:
        await xx.delete()
        await m.reply_text("No birthdays found :/")
        return

    # Sort the users list by the number of days remaining until their birthday
    users.sort(
        key=lambda x: (
            date(curr.year, give_date(x["dob"]).month, give_date(x["dob"]).day) - curr
        ).days
    )

    # Combine today's users with the rest of the users list
    users = today_users + users

    txt = "🎊 Upcoming Birthdays 🎊\n\n"
    for i in users:
        user_id = i["user_id"]
        try:
            user = await c.get_users(user_id)
            first_name = user.first_name
            last_name = user.last_name or ""
            user_link = f"[{first_name} {last_name}](tg://user?id={user_id})"

            dob = give_date(i["dob"])
            birthday = date(curr.year, dob.month, dob.day)
            if birthday == curr:  # Birthday is today
                days_left = "Today is the birthday"
                bday_date = curr.strftime("%B %d")
            else:
                days_left = (birthday - curr).days
                bday_date = birthday.strftime("%B %d")

            txt += f"{days_left} days ({bday_date}) - {user_link}\n"
        except Exception:
            pass

    await xx.delete()
    await m.reply_text(txt, disable_web_page_preview=True)
    return


@app.on_message(command(["getbday", "gbday", "mybirthday", "mybday"]))
async def cant_recall_it(c: app, m: Message):
    if not BDB_URI:
        await m.reply_text("BDB_URI is not configured")
        return
    user = m.from_user.id
    men = m.from_user.mention
    if m.reply_to_message:
        user = m.reply_to_message.from_user.id
        men = m.reply_to_message.from_user.mention
    try:
        result = bday_info.find_one({"user_id": user})
        if not result:
            await m.reply_text("User is not in my database")
            return
    except Exception as e:
        await m.reply_text(f"Got an error\n{e}")
        return

    curr = datetime.now(TIME_ZONE).date()
    u_dob = give_date(result["dob"])
    if u_dob.month < curr.month:
        next_b = date(curr.year + 1, u_dob.month, u_dob.day)
        days_left = (next_b - curr).days
        txt = f"{men} 's birthday is passed 🫤\nDays left until next one {days_left}"
    else:
        u_dobm = date(curr.year, u_dob.month, u_dob.day)
        days_left = (u_dobm - curr).days
        txt = f"User's birthday is coming🥳\nDays left : {days_left}"
    await m.reply_text(txt)
    return


@app.on_message(command(["settingbday", "sbday"]))
async def chat_birthday_settings(c: app, m: Message):
    if not BDB_URI:
        await m.reply_text("BDB_URI is not configured")
        return
    if m.chat.type == ChatType.PRIVATE:
        await m.reply_text("Use in groups")
        return
    chats = m.chat.id
    c_in = bday_cinfo.find_one({"chat_id": chats})
    kb = IKM(
        [
            [
                IKB(
                    f"{'Yes' if not c_in else 'No'}",
                    f"switchh_{'yes' if not c_in else 'no'}",
                ),
                IKB("Close", "f_close"),
            ]
        ]
    )
    await m.reply_text(
        "Do you want to wish members for their birthday in the group?", reply_markup=kb
    )
    return


@app.on_callback_query(filters.regex("^switchh_"))
async def switch_on_off(c: app, q: CallbackQuery):
    user = (await q.message.chat.get_member(q.from_user.id)).status
    await q.message.chat.get_member(q.from_user.id)
    if user not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        await q.answer("...")
        return
    data = q.data.split("_")[1]
    chats = q.message.chat.id
    xXx = {"chat_id": chats}
    if data == "yes":
        bday_cinfo.delete_one(xXx)
    elif data == "no":
        bday_cinfo.insert_one(xXx)
    await q.edit_message_text(
        f"Done! I will {'wish' if data == 'yes' else 'not wish'}",
        reply_markup=IKM([[IKB("Close", "f_close")]]),
    )
    return


scheduler = AsyncIOScheduler()
scheduler.timezone = TIME_ZONE
scheduler_time = time(0, 0, 0)


async def send_wishish(JJK: app):
    c_list = Chats.list_chats_by_id()
    blist = list(bday_info.find())
    curr = datetime.now(TIME_ZONE).date()
    cclist = list(bday_cinfo.find())
    for i in blist:
        dob = give_date(i["dob"])
        if dob.month == curr.month and dob.day == curr.day:
            for j in c_list:
                if cclist and (j in cclist):
                    return
                try:
                    agee = ""
                    if i["is_year"]:
                        agee = curr.year - dob.year
                        if str(agee).endswith("1"):
                            agee = f"{agee}st"
                        elif str(agee).endswith("2"):
                            agee = f"{agee}nd"
                        elif str(agee).endswith("3"):
                            agee = f"{agee}rd"
                        else:
                            agee = f"{agee}th"
                    U = await JJK.get_chat_member(chat_id=j, user_id=i["user_id"])
                    wish = choice(birthday_wish)
                    if U.status in [
                        ChatMemberStatus.MEMBER,
                        ChatMemberStatus.ADMINISTRATOR,
                        ChatMemberStatus.OWNER,
                    ]:
                        xXx = await JJK.send_message(
                            j, f"Happy {agee} birthday {U.user.mention}🥳\n{wish}"
                        )
                        try:
                            await xXx.pin()
                        except Exception:
                            pass
                except Exception:
                    pass


""""
from datetime import date, datetime

#form = 
num = "18/05/2005"
st = "18 May 2005"
timm = datetime.strptime(num,"%d/%m/%Y").date()
x = datetime.now().date()
if timm.month < x.month:
    next_b = date(x.year + 1, timm.month, timm.day)
    days_left = (next_b - x).days
else:
    timmm = date(x.year, timm.month, timm.day)
    days_left = (timmm - x).days
print(days_left)
print(x.year - timm.year)
"""


__PLUGIN__ = "𝗕𝗜𝗥𝗧𝗛𝗗𝗔𝗬"

__HELP__ = """

➥ /remember [reply to user] [DOB] : To registers user date of birth in my database. If not replied to user then the DOB givien will be treated as yours
➥ /nextbdays (/nbdays,/brithdays,/bdays) : Return upcoming birthdays of 10 users
➥ /removebday (/rmbday) : To remove birthday from database (One can only remove their data from database not of others)
➥ /settingbday (/sbday) : To configure the settings for wishing and all for the chat
➥ /getbday (/gbday,/mybirthday,/mybday) [reply to user] : If replied to user get the replied user's birthday else returns your birthday

🎂 DOB should be in format of dd/mm/yyyy
Year is optional it is not necessary to pass it
"""
