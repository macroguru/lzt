from telethon import TelegramClient, events

# Ниже вводите ваши данные с my.telegram.org
api_id = api_id
api_hash = 'api_hash'

client = TelegramClient('picsaver', api_id, api_hash)

@client.on(events.NewMessage)
async def handle_new_message(event):
    message = event.message
    if (
        getattr(message, 'media', False)
        and getattr(message.media, 'ttl_seconds', False)
        and not message.out
    ):
        media = await client.download_media(message.media)
        user_id = message.sender_id
        user_link = f'tg://user?id={user_id}'
        await client.send_file(
            'me',
            media,
            caption=f'🔥[{message.sender.first_name}]({user_link}) отправил вам самоуничтожающееся медиа',
        )

@client.on(events.NewMessage(pattern='.бля')) # Здесь можете сменить команду для ручного сохранения
async def handle_save_command(event):
    message = event.message
    reply = await message.get_reply_message()
    if (
        reply
        and getattr(reply, 'media', False)
        and getattr(reply.media, 'ttl_seconds', False)
    ):
        await message.delete()
        media = await client.download_media(reply.media)
        user_id = reply.sender_id
        user_link = f'tg://user?id={user_id}'
        await client.send_file(
            'me',
            media,
            caption=f'🔥[{reply.sender.first_name}]({user_link}) отправил вам самоуничтожающееся медиа',
        )

async def main():
    await client.start()
    await client.get_dialogs()
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
