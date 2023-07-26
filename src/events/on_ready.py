from client import MyClient
import discord

client: MyClient | None = None


async def on_ready():
    if not client or not client.user:
        return
    await client.change_presence(
        status=discord.Status.offline, afk=True, edit_settings=False
    )
    print(f"Logged as {client.user}\nSelfBot is ready!")
    client.speach.run_queue()
