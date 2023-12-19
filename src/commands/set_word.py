from discord.ext.commands.context import Context as Ctx
from threading import Thread


async def set_word(ctx: Ctx, word: str, fixed_word: str):
	Thread(target=ctx.bot.text.set_word, args=(word, fixed_word)).start()
	await ctx.message.edit(content=f"### Done!\n`{word}` _->_ `{fixed_word}`")
