import asyncio
from client import MyClient
from discord import Message

client: MyClient | None = None


async def on_message(message: Message):
	if not client or message.author != client.user:
		return
	if not message.content.startswith(client.command_prefix.__str__()):
		asyncio.create_task(
			asyncio.to_thread(client.speach.add_to_queue, message.content)
		)

	await client.process_commands(message)
