"""
A module that defines the MyClient class, which is a subclass of discord.Client.
The MyClient class represents a Discord bot client and handles events such as
the bot being ready to start receiving and processing events, and incoming messages.

Classes:
    MyClient

"""
from threading import Thread
import discord
from speach import Speach
from utils.text import Text


class MyClient(discord.Client):
    """
    A subclass of discord.Client that represents a Discord bot client.

    Attributes:
        speach (Speach): An instance of the Speach class.

    Methods:
        __init__: Initializes an instance of the MyClient class.
        on_ready: Asynchronous function called
        when the bot is ready to start receiving and processing events.
        on_message: Handles incoming messages.

    """

    def __init__(self, speach: Speach, text: Text):
        super().__init__()
        self.speach = speach
        self.text = text

    async def on_ready(self):
        """
        Asynchronous function that is called when
        the bot is ready to start receiving and processing events.

        Parameters:
            self (class): The instance of the class that the function belongs to.

        Returns:
            None
        """
        await self.change_presence(
            status=discord.Status.offline,
            afk=True,
            edit_settings=False)
        print('Logged on as', self.user)
        if not self.speach.is_running:
            Thread(target=self.speach.play_queue, daemon=True).start()
            self.speach.is_running = True

    async def on_message(self, message):
        """
        Handle incoming messages.

        Args:
            message: The message object representing the incoming message.

        Returns:
            None
        """
        if message.author != self.user:
            return
        if message.content.startswith('vo!set_word'):
            args = message.content.lower().split()
            Thread(target=self.text.set_word, args=(args[1], args[2])).start()
            return
        Thread(target=self.speach.add_to_queue, args=(message.content,)).start()
