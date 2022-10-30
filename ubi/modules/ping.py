import re
import asyncio
from datetime import datetime
from telethon import events

from ubi import u

@u.on(events.NewMessage(pattern= re.compile(r"\.ping") , outgoing=True))  # pylint: disable=E0602
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Pinging ...")
    print('Pinging')
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(f" Bonk! : `{ms}` ms")
    await asyncio.sleep(1)
    await event.delete()

@u.on(events.NewMessage(pattern=r"\.ping", incoming=True))  # pylint: disable=E0602
async def _(event):
    if event.fwd_from:
        return
    reply = await event.respond("Botto online ... ")
    await asyncio.sleep(1)
    await reply.delete()
