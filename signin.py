from telethon import TelegramClient

# Use your own values from my.telegram.org
api_id = int(input("APP ID: "))
api_hash = input("API HASH: ")

# The first parameter is the .session file name (absolute paths allowed)
with TelegramClient('robisesh', api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message('me', 'Bot logged in !'))