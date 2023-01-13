from telethon import events
from ubi import u, c, l, db , IS_AFK
from datetime import datetime 
from datetime import timedelta

# need to handle global events like getting online and offline soon
# but for now we just do manual commands


# format : .afk some long ass reason |eta: 1xd
@u.on(events.NewMessage(pattern="\.afk (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    # get all the notes and the length
    reason_eta = event.pattern_match.group(1).split("|eta: ")
    reason = reason_eta[0]
    eta = reason_eta[1]
    eta_time = eta.split("x")
    eta_time_int = int(eta_time[0])
    eta_time_chunk = eta_time[1]


    eta_datetime = None
    if (eta_time_chunk == "d"):
        eta_datetime = datetime.now()+timedelta(days=eta_time_int)
    if (eta_time_chunk == "m"):
        eta_datetime = datetime.now()+timedelta(minutes = eta_time_int)
    if (eta_time_chunk == "s"):
        eta_datetime = datetime.now()+timedelta(seconds = eta_time_int)
    if (eta_time_chunk == "h"):
        eta_datetime = datetime.now()+timedelta(hours = eta_time_int)
    if (eta_time_chunk == "w"):
        eta_datetime = datetime.now()+timedelta(weeks = eta_time_int)

    # invalidate previous afk records 
    c.execute("""
    UPDATE afk SET latest = 0 WHERE latest = 1;
    """)
    # add new afk entry 
    c.execute("""
    INSERT INTO afk (reason,eta,afkd,latest)
    VALUES ( ?, ?, datetime('now'), 1 );
    """, (reason , eta_datetime))
    db.commit()

    IS_AFK = True
    # await event.delete()
    await event.edit(f"Going afk for approximately {eta} \nBecause : {reason} ... ")


@u.on(events.NewMessage(pattern="\.test", outgoing=True))
async def _(event):
    
    print("ack")
    await event.delete()
    if event.fwd_from:
        return
    if isinstance(event, events.MessageEdited):
        return
    command = "SELECT * from afk "
    res = c.execute(command).fetchall()
    print(res)

    for line in res:
        await event.respond(f"{line}")

    db.commit()
