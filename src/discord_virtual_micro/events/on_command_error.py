from discord.ext.commands.context import Context as Ctx

from ..abc.event import Event
from ..client import MyClient
from ..utils.module import default


@default
class OnCommandError(Event):
    def __init__(self, client: MyClient) -> None:
        super().__init__(client)

    async def handler(self, ctx: Ctx, error: Exception) -> None:
        await ctx.message.edit(content=str(error))
