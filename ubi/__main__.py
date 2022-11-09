import asyncio
import time
import sys
import importlib
import importlib.util
from pprint import pprint
from ubi import u, l, s , c
from ubi.modules import ALL_MODULES

loop = asyncio.get_event_loop()
LOADED_MODS = []


async def load_module(modul):
    l.info(f"💾 Loading : {modul}")
    importlib.import_module("ubi.modules." + modul)


async def unload_module(modul):
    pass


async def main():
    await u.start()
    for modul in ALL_MODULES:
        await load_module(modul)
        LOADED_MODS.append(modul)

    me = await u.get_me()
    fname = me.first_name if me.first_name else ''
    lname = me.last_name if me.last_name else ''
    uname = me.username if me.username else ''
    uid = str(me.id) if me.id else ''
    isbot = "🔥" if not me.bot else "🤖"

    l.info(
        f"{isbot} Ubi Ready and linked to ⎣ {fname + lname + ' @'+ uname + ' ' + uid} ⎤ ")
    await u.run_until_disconnected()


if __name__ == '__main__':
    BOT_RUNTIME = int(time.time())
    try:
        loop.run_until_complete(main())

    except KeyboardInterrupt:
        l.info("🧹 Closing db cursor !")
        c.close()
        l.info("🧹 Shutting down Scheduler !")
        s.shutdown()
        l.info("💀 Bot Dead !")
