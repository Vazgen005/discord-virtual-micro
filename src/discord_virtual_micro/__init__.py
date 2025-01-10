"""
This module contains the main function for running a speech synthesis client.

It reads a configuration file, loads a pre-trained model,
and initializes a speech synthesis system. It then creates a client and runs it.
"""

import asyncio
import json
import logging
import os
from shutil import copyfile
import sys
from pathlib import Path
from .utils.config import _Speaker

import torch
from aiorun import run
from silero import silero_tts

from .client import MyClient
from .speach import Speach
from .utils.patcher import patch_all
from .utils.text import Text
from .utils.config import get_virtual, get_physical


async def start() -> int:
    """
    The start function reads a configuration file, loads a pre-trained model,
    and initializes a speech synthesis system. It then creates a client and runs it.

    Parameters:
    None

    Returns:
    None
    """
    patch_all()
    loop = asyncio.get_event_loop()
    if os.path.exists("config.json"):
        with open("config.json", "r", encoding="utf-8") as file:
            config = json.load(file)
    else:
        copyfile(Path(__file__).parent / "config-example.json", "config.json")
        print("Please fill in the necessary details in the config.json file.")
        loop.stop()
        return 1

    virtual: _Speaker | None = get_virtual(config["virtual"])
    physical: _Speaker | None = get_physical(config["physical"])

    error_msg = "Your {} is not found. Please check the config.json file."
    if not virtual:
        print(error_msg.format("virtual microphone"))
        loop.stop()
        return 1
    if not physical:
        print(error_msg.format("physical speaker"))
        loop.stop()
        return 1

    model, *_ = silero_tts(
        language=config["language"],
        speaker=config["model_id"],
        device="cuda:0" if torch.cuda.is_available() else "cpu",
    )

    text = Text(config["link_replacement"], config["transliterate_to"])

    speach = Speach(
        model=model,
        virtual=virtual,
        physical=physical,
        sample_rate=config["sample_rate"],
        play_on_pysical=config["play_on_pysical"],
        speaker=config["speaker"],
        delay_after=config["delay_after"],
        on_fail=config["on_fail"],
        text=text,
        loop=loop,
    )
    speach.add_to_queue(config["on_ready"])

    logging.basicConfig(level=logging.INFO)

    await MyClient(speach=speach, text=text).start(token=config["dc_token"])
    loop.close()
    return 0


def main():
    sys.exit(run(start(), stop_on_unhandled_errors=True))
