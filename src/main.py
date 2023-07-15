"""
This module contains the main function for running a speech synthesis client.

It reads a configuration file, loads a pre-trained model,
and initializes a speech synthesis system. It then creates a client and runs it.
"""
import sys
import json
import torch
import soundcard as sc
from speach import Speach
from client import MyClient
from utils.text import Text


def main():
    """
    The main function reads a configuration file, loads a pre-trained model,
    and initializes a speech synthesis system. It then creates a client and runs it.

    Parameters:
    None

    Returns:
    None
    """
    try:
        with open('config.json', 'r', encoding='utf-8') as file:
            config = json.load(file)
    except OSError as ex:
        print(f"Could not load config.json\n{ex}")
        sys.exit(1)

    model, _ = torch.hub.load(
        repo_or_dir='snakers4/silero-models',
        model='silero_tts',
        language=config["language"],
        speaker=config["model_id"],
        trust_repo=True)

    torch._C._jit_set_profiling_mode(False)  # type: ignore

    text = Text()
    speach = Speach(
        model=model,
        virtual=sc.get_speaker(config["virtual"]),
        physical=sc.get_speaker(config["physical"]),
        sample_rate=config["sample_rate"],
        play_on_pysical=config["play_on_pysical"],
        speaker=config["speaker"],
        delay_after=config["delay_after"],
        on_fail=config["on_fail"],
        text=text)
    speach.add_to_queue(config["on_ready"])
    client = MyClient(speach, text)
    client.run(config["dc_token"])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
