''' Cat pictures and gifs '''

import requests
from telethon import events

from ubi import u 

url = ' https://api.thecatapi.com/v1/images/search'
url_gif = ' https://api.thecatapi.com/v1/images/search?mime_types=gif'

@u.on(events.NewMessage(pattern=r"\.cat"))
async def _(event):
    if event.fwd_from:
        return
    out = event.message.out 
    response = requests.get(url)
    data = response.json()
    data = data[0]
    entity = await event.get_input_chat()
    if out : await event.delete()
    await u.send_message(
        entity=entity,
        file=data['url'] )

@u.on(events.NewMessage(pattern=r"\.gat"))
async def _(event):
    out = event.message.out
    if event.fwd_from:
        return
    response = requests.get(url_gif)
    data = response.json()
    data = data[0]
    entity = await event.get_input_chat()
    if out : await event.delete()
    await u.send_message(
        entity=entity,
        file=data['url'] )

