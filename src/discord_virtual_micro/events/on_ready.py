import asyncio

import discord

from ..abc.event import Event
from ..client import MyClient
from ..utils.module import default


@default
class OnReady(Event):
    def __init__(self, client: MyClient) -> None:
        super().__init__(client)

    async def handler(self) -> None:
        await self.client.change_presence(
            status=discord.Status.offline, afk=True, edit_settings=False
        )
        print(f"Logged as {self.client.user}\nSelfBot is ready!")
        asyncio.create_task(self.client.speach.run_queue())
