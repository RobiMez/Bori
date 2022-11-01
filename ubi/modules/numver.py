''' Phone verification plugin '''

import asyncio
import re
from telethon import events
from telethon.tl.types import InputPeerUser
from ubi import u, s

del_timeout = 6
@u.on(events.NewMessage(pattern=r"\.nv (.*)|\.nv"))
async def _(event):
    if event.fwd_from:
        return
    out = event.message.out
    para = event.pattern_match.group(1)
    para_split = para.split(" ")
    # check for digit-ness
    if not para or len(para_split) < 2 or \
            not para_split[1].isdigit() or not para_split[0].isdigit():
        if out:
            await event.edit("Usage : `.nv 251910101010 <code>`")
            await asyncio.sleep(del_timeout)
            await event.delete()
        else:
            await event.respond("Usage : `.nv 251910101010 <code>`")
    else:
        await event.edit("Checking entity")
        # Take phone number and try get its entity
        try:
            ent = await u.get_input_entity(para_split[0])
            if isinstance(ent, InputPeerUser):
                if out:
                    await event.edit("Sending code ")
                    await u.send_message(ent, f"Verification code : `{para_split[1]}`")
                    await event.edit("Sent code!")
                    await asyncio.sleep(del_timeout)
                    await event.delete()
                else :
                    resp = await event.respond("Sending code ...")
                    await u.send_message(ent, f"Verification code : `{para_split[1]}`")
                    await resp.edit("Sent code!")
                    await asyncio.sleep(del_timeout)
                    await resp.delete()
            else:
                resp = await event.respond("Not a valid phone number or user doesnt have telegram installed.")
                await asyncio.sleep(del_timeout)
                await resp.delete()
        except ValueError:
                resp = await event.respond("Not a valid phone number or user doesnt have telegram installed.")
                await asyncio.sleep(del_timeout)
                await resp.delete()