"""Global thingies get defined here"""

import os
import re
import sqlite3
import logging
import pymongo

from pytz import utc
from pathlib import Path
from dotenv import load_dotenv

from telethon import TelegramClient, events
from telethon.sessions import StringSession

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

load_dotenv(dotenv_path=Path('.env'))

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
SESH = os.environ.get("SESH")
DB_URL = os.environ.get("DB_URL")
MDB_URL = os.environ.get("MDB_URL")


# LOGGER ----------------------------------------------------------------------------------
LOG_FORMAT = "[%(asctime)s.%(msecs)03d] %(filename)s:%(lineno)s %(levelname)s: %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt='%m-%d %H:%M',)

l = logging.getLogger()
# LOGGER ----------------------------------------------------------------------------------


# SCHEDULER -------------------------------------------------------------------------------
jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
s = AsyncIOScheduler(daemon=True, jobstores=jobstores, timezone=utc)
s.start()


def admin_cmd(pattern):
    return events.NewMessage(outgoing=True, pattern=re.compile(pattern))
# SCHEDULER -------------------------------------------------------------------------------


# DATABASES --------------------------------------------------------------------------------
db = sqlite3.connect(DB_URL)
c = db.cursor()

m = pymongo.MongoClient(MDB_URL)

# Create operation
create_query = '''CREATE TABLE if not exists afk (
  ID INTEGER PRIMARY KEY,
  reason TEXT,
  eta DATETIME,
  afkd DATETIME,
  latest BOOL
  );
  '''
c.execute(create_query)

# Write a query and execute it with cursor
query = 'select sqlite_version();'
c.execute(query)
# Fetch and output result
result = c.fetchall()
l.info(f'SQLite Version is {result[0][0]}')
# DATABASES --------------------------------------------------------------------------------


# TELEGRAM CLIENT -------------------------------------------------------------------------
USERBOT_LOAD = []
USERBOT_NOLOAD = []

u: TelegramClient = TelegramClient(
    api_id=int(API_ID), api_hash=API_HASH, session=StringSession(SESH)).start()
# TELEGRAM CLIENT -------------------------------------------------------------------------


# STATES ----------------------------------------------------------------------------------
res = c.execute("SELECT * from afk where latest=1").fetchone()

if res == None:
    IS_AFK = False
else:
    IS_AFK = True


# STATES ----------------------------------------------------------------------------------
