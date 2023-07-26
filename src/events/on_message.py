from threading import Thread
from client import MyClient
from discord import Message

client: MyClient | None = None


async def on_message(message: Message):
    if not client or not (message.author == client.user):
        return
    if message.content.startswith(client.command_prefix.__str__()):
        await client.process_commands(message)
        return

    Thread(target=client.speach.add_to_queue, args=(message.content,)).start()

    await client.process_commands(message)
