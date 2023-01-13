from telethon import events
from ubi import u 
import  re 


@u.on(events.NewMessage(pattern= re.compile(r"\.die")))  # pylint: disable=E0602
async def _(event):
    if event.fwd_from:
        return
    await event.reply("Commiting Soduku ... 💀")
    await u.disconnect()
