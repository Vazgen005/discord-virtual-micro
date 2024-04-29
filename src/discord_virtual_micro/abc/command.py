from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from discord.ext.commands.context import Context as Ctx

if TYPE_CHECKING:
    from ..client import MyClient
from ..utils.text import pascal_to_snake


class Command(ABC):
    def __init__(self, client: "MyClient") -> None:
        self.client: MyClient = client
        self.name: str = pascal_to_snake(self.__class__.__name__)

    @abstractmethod
    async def handler(self, ctx: Ctx, *args: str) -> None: ...
