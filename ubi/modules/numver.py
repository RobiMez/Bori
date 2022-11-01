''' Phone verification plugin '''

import asyncio
import re
from telethon import events
from telethon.tl.types import InputPeerUser
from ubi import u, s


@u.on(events.NewMessage(pattern=r"\.nv (.*)|\.nv"))
async def _(event):
    if event.fwd_from:
        return
    out = event.message.out
    para = event.pattern_match.group(1)
    para_split = para.split(" ")
    # check for digit-ness 
    if not para or len(para_split) < 2  or \
        not para_split[1].isdigit()  or not para_split[0].isdigit():
        if out:
            await event.edit("Usage : `.nv 251910101010 <code>`")
            await asyncio.sleep(4)
            await event.delete()
        else:
            await event.respond("Usage : `.nv 251910101010 <code>`")
    else:
        await event.edit("Checking entity")
        # Take phone number and try get its entity
        try:
            ent = await u.get_input_entity(para_split[0])
            if isinstance(ent, InputPeerUser):
                await event.edit("Sending code ")
                await u.send_message(ent , f"Verification code : `{para_split[1]}`")
                await event.edit("Sent code!")
            else:
                await event.edit("Not a valid phone number or user doesnt have telegram installed.")
        except ValueError:
            await event.edit("Not a valid phone number or user doesnt have telegram installed.")


