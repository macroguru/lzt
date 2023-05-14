from telethon import TelegramClient, events
import random

api_id = id
api_hash = 'hash'

client = TelegramClient('tagall_session', api_id, api_hash)
client.start()

@client.on(events.NewMessage(pattern='!tagall'))
async def tag_all(event):
    if event.sender_id != (await client.get_me()).id:
        return
    
    chat = await event.get_chat()
    text = event.text.partition(' ')[2] if ' ' in event.text else 'Внимание всем!'
    mentions = ''.join(f'[{random.choice(["❤️","🌕","🌚","🌑","🌝","🔆","✅","♦️","♣️","♠️","🌟","💫"])}](tg://user?id={m.id}) ' for m in await event.client.get_participants(await event.get_chat()))
    await client.send_message(chat, f'**{text}** {mentions}')
    await event.delete()

client.run_until_disconnected()