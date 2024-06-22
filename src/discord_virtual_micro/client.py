"""
A module that defines the MyClient class, which is a subclass of discord.Client.
The MyClient class represents a Discord bot client and handles events such as
the bot being ready to start receiving and processing events, and incoming messages.

Classes:
        MyClient

"""

import logging
from pathlib import Path
from types import ModuleType
from typing import cast

from discord.ext import commands
from discord.ext.commands import Command as DiscordCommand

from .abc.command import Command
from .abc.event import Event
from .speach import Speach
from .utils.module import get_default_class, import_file
from .utils.text import Text


class MyClient(commands.Bot):
    def __init__(self, speach: Speach, text: Text) -> None:
        self.logger = logging.getLogger(__name__)
        super().__init__(command_prefix="vo!", self_bot=True)
        self.speach = speach
        self.text = text
        self.__commands_path = Path(__file__).parent / "commands"
        self.__events_path = Path(__file__).parent / "events"
        self.__package_name = __name__.split(".")[0]
        self.__load_commands()
        self.__load_events()

    def __load_commands(self) -> None:
        for file in self.__commands_path.glob("*.py"):
            module_name: str = f"{self.__package_name}.commands.{file.stem}"
            module: ModuleType = import_file(str(file), module_name)
            if default_class := get_default_class(module):
                command_obj: Command = cast("Command", default_class(self))
                discord_command = DiscordCommand(
                    command_obj.handler, name=command_obj.name
                )
                self.add_command(discord_command)
                self.logger.info(f"Loaded {command_obj.name} command")

    def __load_events(self) -> None:
        for file in self.__events_path.glob("*.py"):
            module_name = f"{self.__package_name}.events.{file.stem}"
            module: ModuleType = import_file(str(file), module_name)
            if default_class := get_default_class(module):
                event_obj: Event = cast("Event", default_class(self))
                setattr(
                    getattr(event_obj.handler, "__func__"), "__name__", event_obj.name
                )
                self.event(event_obj.handler)
                self.logger.info(f"Loaded {event_obj.name} event")
