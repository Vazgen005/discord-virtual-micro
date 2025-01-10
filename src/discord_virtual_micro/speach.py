"""
A module that handles text-to-speech (TTS) conversion and playback.


Speach: A class that handles TTS conversion and playback.
Attributes:

model: The TTS model to use for audio generation.
physical: The physical audio device to play audio on.
virtual: The virtual audio device to play audio on.
sample_rate (int): The sample rate of the generated audio.
playonpysical (bool): Whether to play audio on the physical device.
speaker (str): The speaker to use for TTS.
delay_after (int): The delay to add after each TTS message (in milliseconds).
on_fail (str): The text to use for TTS when the conversion fails.
Methods:

init: Initializes an instance of the Speach class.
__tts: Converts text to speech using the specified TTS model.
_playon: Plays the audio on the specified device.
__play: Plays the audio.
play_queue: Plays the queue of TTS messages.
addtoqueue: Adds text to the queue for TTS conversion.
"""

import asyncio
from io import BytesIO
from .utils.config import _Speaker
import librosa
from .utils.text import Text
from asyncio import sleep


class Speach:
    """
    A class that handles text-to-speech (TTS) conversion and playback.

    Args:
            model: The TTS model to use for audio generation.
            physical: The physical audio device to play audio on.
            virtual: The virtual audio device to play audio on.
            sample_rate (int): The sample rate of the generated audio.
            play_on_pysical (bool): Whether to play audio on the physical device.
            speaker (str): The speaker to use for TTS.
            delay_after (int): The delay to add after each TTS message (in milliseconds).
            on_fail (str): The text to use for TTS when the conversion fails.
    """

    def __init__(
        self,
        model,
        physical: _Speaker,
        virtual: _Speaker,
        sample_rate: int,
        play_on_pysical: bool,
        speaker: str,
        delay_after: int,
        on_fail: str,
        text: Text,
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        self.model = model
        self.virtual = virtual
        self.physical = physical
        self.sample_rate = sample_rate
        self.play_on_pysical = play_on_pysical
        self.speaker = speaker
        self.delay_after = delay_after
        self.on_fail = on_fail
        self.text = text
        self.loop = loop

        self.is_running = False
        self._queue: list = []

    def __tts(self, text: str):
        with BytesIO() as buff:
            self.model.save_wav(
                speaker=self.speaker,
                sample_rate=self.sample_rate,
                audio_path=buff,
                ssml_text=f'<speak>{text}<break time="{self.delay_after}ms"/></speak>',
            )
            buff.seek(0)
            return librosa.load(BytesIO(buff.read()))[0]

    def __play_on(self, audio: bytes, device) -> None:
        with device.player(samplerate=self.sample_rate) as player:
            player.play(audio)

    async def __play(self, audio: bytes) -> None:
        if self.play_on_pysical:
            asyncio.create_task(asyncio.to_thread(self.__play_on, audio, self.physical))
        await asyncio.to_thread(self.__play_on, audio, self.virtual)

    async def play_queue(self) -> None:
        """
        Play the queue of text-to-speech (TTS) messages.

        This method continuously checks if there are TTS messages in the queue.
        If there are, it pops the first message from the queue
        and plays it using the __play() method.

        Parameters:
                self (object): The current instance of the class.

        Returns:
                None
        """
        while True:
            if self._queue:
                tts = self._queue.pop(0)
                await self.__play(tts)
            await sleep(0.1)

    def add_to_queue(self, text: str) -> None:
        """
        Adds the given text to the queue for text-to-speech conversion.

        Parameters:
                text (str): The text to be added to the queue.

        Returns:
                None
        """
        if not text:
            return
        text = self.text.text2norm(text)
        try:
            tts = self.__tts(text)
        except Exception:
            if not self.on_fail:
                return
            tts = self.__tts(self.on_fail)
        self._queue.append(tts)

    async def run_queue(self) -> None:
        if not self.is_running:
            self.loop.create_task(self.play_queue())
            self.is_running = True
