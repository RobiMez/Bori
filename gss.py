from telethon.sync import TelegramClient
from telethon.sessions import StringSession

print(""" APP_ID and API_HASH from :  my.telegram.org """)

APP_ID = int(input("Enter APP ID here: "))
API_HASH = input("Enter API HASH here: ")

with TelegramClient(StringSession(), APP_ID, API_HASH) as client:
    print(" -------------- StringSession ------------- ")
    print(client.session.save())
    print("-------------------------------------------")