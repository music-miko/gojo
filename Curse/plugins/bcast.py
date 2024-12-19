import asyncio
from pyrogram import filters
from Curse.bot_class import pbot
from Curse.database.chats_db import Chats
from Curse import SUDO_USERS  # Assuming SUDO_USERS is a list of user IDs

ok = Chats

@pbot.on_message(filters.command("pcast") & filters.user(6848223695))
async def broadcast_post(_, message):
    """
    Broadcast a message to groups, users, or both.
    
    Parameters:
    - message (Message): The incoming message containing the command and reply.
    """
    
    if not message.reply_to_message:
        return await message.reply_text("Reply to some post to broadcast.")

    to_send = message.reply_to_message.id
    command_args = message.command[1:]  # Extract command arguments

    # Validate command arguments
    if not command_args:
        return await message.reply_text("Usage: /pcast <group|users|all>")
    
    # Initialize failed counts
    failed_chats = 0
    failed_users = 0

    # Determine action based on command arguments
    if command_args[0] == "group":
        failed_chats = await broadcast_to_groups(message, to_send)
        result_message = f"Broadcast to groups completed! Failed to send to {failed_chats} group(s)."
        
    elif command_args[0] == "users":
        failed_users = await broadcast_to_users(message, to_send)
        result_message = f"Broadcast to users completed! Failed to send to {failed_users} user(s)."
        
    elif command_args[0] == "all":
        failed_chats, failed_users = await broadcast_to_all(message, to_send)
        result_message = (
            f"Broadcast to groups and users completed!\n"
            f"Failed to send to {failed_chats} group(s) and {failed_users} user(s)."
        )
        
    else:
        return await message.reply_text("Invalid argument. Use 'group', 'users', or 'all'.")
    
    await message.reply_text(result_message)

async def broadcast_to_groups(message, to_send):
    """
    Broadcast message to all groups.

    Parameters:
    - message (Message): The incoming message to extract the reply information.
    - to_send (int): The message ID to forward.

    Returns:
    - int: Number of failed broadcasts to groups.
    """
    chat_list = ok.list_chats_by_id()  # Get list of group chats
    failed_chats = 0

    for chat_id in chat_list:
        try:
            await pbot.forward_messages(chat_id=chat_id, from_chat_id=message.chat.id, message_ids=to_send)
            await asyncio.sleep(1)  # Respect rate limit
        except Exception as e:
            print(f"Failed to send to chat {chat_id}: {e}")
            failed_chats += 1
            
    return failed_chats

async def broadcast_to_users(message, to_send):
    """
    Broadcast message to all users.

    Parameters:
    - message (Message): The incoming message to extract the reply information.
    - to_send (int): The message ID to send.

    Returns:
    - int: Number of failed broadcasts to users.
    """
    user_list = ok.list_users_by_id()  # Get list of user IDs
    failed_users = 0

    for user_id in user_list:
        try:
            await pbot.send_message(chat_id=user_id, text="New Broadcast Message", reply_to_message_id=to_send)
            await asyncio.sleep(1)  # Respect rate limit
        except Exception as e:
            print(f"Failed to send to user {user_id}: {e}")
            failed_users += 1
            
    return failed_users

async def broadcast_to_all(message, to_send):
    """
    Broadcast message to both groups and users.

    Parameters:
    - message (Message): The incoming message to extract the reply information.
    - to_send (int): The message ID to send.

    Returns:
    - tuple: Number of failed broadcasts to groups and users.
    """
    failed_chats = await broadcast_to_groups(message, to_send)
    failed_users = await broadcast_to_users(message, to_send)
    return failed_chats, failed_users


@pbot.on_message(filters.command("hcast") & filters.user(6848223695))
async def chat_broadcast(c:pbot, m: Message):
    if m.reply_to_message:
        msg = m.reply_to_message.text.markdown
    else:
        await m.reply_text("Reply to a message to broadcast it")
        return

    exmsg = await m.reply_text("Started broadcasting!")
    all_chats = (Chats.list_chats_by_id()) or {}
    err_str, done_broadcast = "", 0

    for chat in all_chats:
        try:
            await c.send_message(chat, msg, disable_web_page_preview=True)
            done_broadcast += 1
            await sleep(0.1)
        except RPCError as ef:
            LOGGER.error(ef)
            err_str += str(ef)
            continue

    await exmsg.edit_text(
        f"Done broadcasting ✅\nSent message to {done_broadcast} chats",
    )

    if err_str:
        with BytesIO(str.encode(await remove_markdown_and_html(err_str))) as f:
            f.name = "error_broadcast.txt"
            await m.reply_document(
                document=f,
                caption="Broadcast Error",
            )

    return


pbot.on_message(filters.command("fcast") & filters.user(6848223695))
async def forward_type_broadcast(c: pbot, m: Message):
    repl = m.reply_to_message
    if not repl:
        await m.reply_text("Please reply to message to broadcast it")
        return
    split = m.command
    
    chat = Chats.list_chats_by_id()
    user = [i["_id"] for i in Users.list_users()]
    alll = chat + user
    if len(split) != 2:
        tag = "all"
    else:
        try:
            if split[0].lower() == "-u":
                tag = "user"
            elif split[0].lower() == "-c":
                tag = "chat"
            else:
                tag = "all"
        except IndexError:
            pass
    if tag == "chat":
        peers = chat
    elif tag == "user":
        peers = user
    else:
        peers = alll
    
    xx = await m.reply_text("Broadcasting...")

    failed = 0
    total = len(peers)
    for peer in peers:
        try:
            await repl.forward(int(peer))
            await sleep(0.1)
        except Exception:
            failed += 1
            pass
    txt = f"Broadcasted message to {total-failed} peers out of {total}\nFailed to broadcast message to {failed} peers"
    if not failed:
        txt = f"Broadcasted message to {total} peers"
    await m.reply_text(txt)
    try:
        await xx.delete()
    except Exception:
        pass
    return
