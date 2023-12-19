from discord.ext.commands.context import Context as Ctx


async def del_word(ctx: Ctx, word: str):
	deleted = ctx.bot.text.del_word(word)
	if deleted:
		await ctx.message.edit(content=f"### Done\n`{word}` ⤫ `{deleted}`")
		return
	await ctx.message.edit(content=f"### Error\n`{word}` not found in the dictionary")
