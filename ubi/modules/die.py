from telethon import events
from ubi import u 
from datetime import datetime
import asyncio


@u.on(events.NewMessage(pattern= re.compile(r"\.ping") , outgoing=True))  # pylint: disable=E0602
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Okay ;< ...")
    u.disconnect()
