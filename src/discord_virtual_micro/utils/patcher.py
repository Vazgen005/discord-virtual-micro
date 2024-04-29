import discord
import discord.ext
import discord.ext.commands

from ..patches.get_signature_parameters import (
    get_signature_parameters as patched_get_signature_parameters,
)


def patch_all() -> None:
    discord.ext.commands.core.get_signature_parameters = (
        patched_get_signature_parameters
    )
