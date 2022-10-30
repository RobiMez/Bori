import imp
import os
import logging
from pathlib import Path
from telethon import TelegramClient, connection, events
from telethon.sessions import StringSession
from dotenv import load_dotenv
import re


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from pytz import utc

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
s = AsyncIOScheduler(daemon=True, jobstores=jobstores, timezone=utc)


def admin_cmd(pattern):
    return events.NewMessage(outgoing=True, pattern=re.compile(pattern))


load_dotenv(dotenv_path=Path('.env'))

# APP_SESSION = "ubi"
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
SESH = os.environ.get("SESH")

USERBOT_LOAD = []
USERBOT_NOLOAD = []

u : TelegramClient = TelegramClient(api_id=int(API_ID), api_hash=API_HASH, session=StringSession(SESH)).start()

LOG_FORMAT = "[%(asctime)s.%(msecs)03d] %(filename)s:%(lineno)s %(levelname)s: %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt='%m-%d %H:%M',)

log = logging.getLogger()
