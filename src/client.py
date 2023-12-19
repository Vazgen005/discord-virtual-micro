"""
A module that defines the MyClient class, which is a subclass of discord.Client.
The MyClient class represents a Discord bot client and handles events such as
the bot being ready to start receiving and processing events, and incoming messages.

Classes:
	MyClient

"""
from discord.ext import commands
from discord.ext.commands import Command
from speach import Speach
from utils.text import Text
from pathlib import Path
from pydoc import importfile
import logging


class MyClient(commands.Bot):
	def __init__(self, speach: Speach, text: Text) -> None:
		self.logger = logging.getLogger(__name__)
		super().__init__(command_prefix="vo!", self_bot=True)
		self.speach = speach
		self.text = text
		self.__commands_path = Path(__file__).parent / "commands"
		self.__events_path = Path(__file__).parent / "events"
		self.__load_commands()
		self.__load_events()

	def __load_commands(self) -> None:
		for file in self.__commands_path.glob("*.py"):
			module = importfile(file.__str__())
			command = Command(getattr(module, module.__name__))
			self.add_command(command)
			self.logger.info(f"Loaded {module.__name__} command")

	def __load_events(self) -> None:
		for file in self.__events_path.glob("*.py"):
			module = importfile(file.__str__())
			module.client = self  # type: ignore
			func = getattr(module, module.__name__)
			self.event(func)
			self.logger.info(f"Loaded {module.__name__} event")
