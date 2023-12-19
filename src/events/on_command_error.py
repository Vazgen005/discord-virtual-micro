from discord.ext import commands
from discord.ext.commands import errors
from discord.ext.commands.context import Context as Ctx
from client import MyClient

client: MyClient | None = None


async def on_command_error(ctx: Ctx, error: Exception):
	await ctx.message.edit(content=str(error))
