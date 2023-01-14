from telethon import events
from ubi import u
import re
from ubi.modules.strings import KILL_CODE


@u.on(events.NewMessage(pattern=re.compile(r"\.die (.*)")))
async def _(event):
    if event.fwd_from:
        return
    killcode = event.pattern_match.group(1)
    print(killcode)
    if killcode == KILL_CODE:
        await event.reply("Valid Killcode Entered  ... \nDisconnecting ! 💀")
        await u.disconnect()
    else:
        await event.reply("Kill Code Invalid  ... \n")
