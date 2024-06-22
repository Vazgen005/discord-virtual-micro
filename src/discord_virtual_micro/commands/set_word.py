from asyncio import to_thread

from discord.ext.commands.context import Context as Ctx
from ..client import MyClient

from ..abc.command import Command
from ..utils.module import default


@default
class SetWord(Command):
    def __init__(self, client: MyClient) -> None:
        super().__init__(client)

    async def handler(self, ctx: Ctx, word: str, fixed_word: str) -> None:
        await to_thread(self.client.text.set_word, word, fixed_word)
        await ctx.message.edit(content=f"### Done!\n`{word}` _->_ `{fixed_word}`")
