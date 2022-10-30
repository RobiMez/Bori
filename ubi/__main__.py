import asyncio
import time
import importlib

from ubi import u, log , s
from ubi.modules import ALL_MODULES

loop = asyncio.get_event_loop()


async def main():
    await u.start()
    for modul in ALL_MODULES:
        log.info(f"💾 Loading : {modul}")
        importlib.import_module("ubi.modules." + modul)

    me = await u.get_me()
    fname = me.first_name if me.first_name else ''
    lname = me.last_name if me.last_name else ''
    uname = me.username if me.username else ''
    uid = str(me.id) if me.id else ''
    isbot = "🔥" if not me.bot else "🤖"

    log.info(
        f"{isbot} Ubi Ready and linked to ⎣ {fname + lname + ' @'+ uname + ' ' + uid} ⎤ ")
    await u.run_until_disconnected()



if __name__ == '__main__':
    BOT_RUNTIME = int(time.time())
    try:
        s.start()
        loop.run_until_complete(main())

    except KeyboardInterrupt:
        # log.info("🧹 Removing all jobs !")
        # s.remove_all_jobs()
        log.info("🧹 Shutting down Scheduler !")
        s.shutdown()
        log.info("💀 Bot Dead !")
