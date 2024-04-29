from asyncio import to_thread

from discord.ext.commands.context import Context as Ctx
from ..client import MyClient

from ..abc.command import Command
from ..utils.module import default


@default
class DelWord(Command):
    def __init__(self, client: MyClient) -> None:
        super().__init__(client)

    async def handler(self, ctx: Ctx, word: str) -> None:
        deleted = await to_thread(self.client.text.del_word, word)
        if deleted:
            await ctx.message.edit(content=f"### Done\n`{word}` ⤫ `{deleted}`")
            return
        await ctx.message.edit(
            content=f"### Error\n`{word}` not found in the dictionary"
        )
