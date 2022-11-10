from telethon import events
from telethon.tl.types import UpdateUserStatus , UserStatusOnline , UserStatusOffline 
import asyncio
from datetime import datetime
from ubi import u, c, l, db , m

notified_afk = []

@u.on(events.NewMessage(incoming=True, func=lambda e: bool(
    (e.mentioned or e.is_private) and True if c.execute("SELECT * from afk where latest=1").fetchone() != None else False)))
async def reply_on_afk(event):
    uid = None
    if hasattr(event.original_update, "user_id"):
        uid = event.original_update.user_id
    elif hasattr(event.original_update, "from_id"):
        uid = event.original_update.from_id

    if uid not in notified_afk:
        command = "SELECT * from afk where latest=1"
        res = c.execute(command).fetchone()
        if not res == None:
            print(res)
        date_offline = datetime.strptime(res[3], '%Y-%m-%d %H:%M:%S')
        date_eta = datetime.strptime(res[2], '%Y-%m-%d %H:%M:%S.%f')
        print(date_eta)
        print(date_offline)

        tdiff = date_eta - date_offline

        await event.reply("**Robi is currently unavailable** \n"
                          f" Reason given : __{res[1]}__\n"
                          f" Back by : `{res[2]}`\n"
                          f" Went offline at : `{res[3]}`\n\n"

                          f"__This is an automated response__\n"
                          "__This message should only display once per user , in private messages or when someone replies to me in a group . Please mute me if anything malufunctions , thanks .__"
                          )
        notified_afk.append(uid)


@u.on(events.NewMessage(outgoing=True, func=lambda e: True if c.execute("SELECT * from afk where latest=1").fetchone() != None else False))
async def unafk(event):
    print(event.original_update.message.message[:3])
    print(type(event))
    if isinstance(event, events.MessageEdited):
        return
    if event.original_update.message.message[:4] == ".afk":
        return
    print(f"unafking ...")
    c.execute("""
    UPDATE afk SET latest = 0 WHERE latest = 1;
    """)
    msg = await event.reply("Unset afk.")
    await asyncio.sleep(2)
    await msg.delete()


@u.on(events.UserUpdate)
async def user_update_handler(event):
    # mdb = m.statusChanges
    print("\n")
    print(event.stringify())
    print("\n")
    print(await u.get_me().id)
    if isinstance(event.original_update ==  UpdateUserStatus) : 
        print("Update is a user status update")

    # print(f"{event.original_update.user_id}")
