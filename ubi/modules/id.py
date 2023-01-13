import re
from telethon import events
from ubi import u

@u.on(events.NewMessage(pattern=r"\.id ?(.*)", outgoing=True))  
async def _(event):
    # if forwarded message
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str:
        try:
            chat = await u.get_entity(input_str)  
        except Exception as e:
            await event.edit(str(e))
            return None
        else:
            f"{input_str} Chat ID: `{str(chat.id)}`\n"
    if event.reply_to_msg_id:
        r_msg = await event.get_reply_message()
        if r_msg.media:
            pass
        else:
            chat = await event.get_input_chat()
            await event.edit(
                f"Current Chat_ID is `{str(event.chat_id)}` \n"
                f"User_ID: `{str(r_msg.from_id)}`"
            )
    else:
        chat = await event.get_input_chat()
        await event.edit(f"This chat has id : `{str(event.chat_id)}`")
