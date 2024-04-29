import asyncio

from discord import Message

from ..abc.event import Event
from ..client import MyClient
from ..utils.module import default


@default
class OnMessage(Event):
    def __init__(self, client: MyClient) -> None:
        super().__init__(client)

    async def handler(self, message: Message) -> None:
        if message.author != self.client.user or message.content.startswith(
            str(self.client.command_prefix)
        ):
            await self.client.process_commands(message)
            return
        asyncio.create_task(
            asyncio.to_thread(self.client.speach.add_to_queue, message.content)
        )
