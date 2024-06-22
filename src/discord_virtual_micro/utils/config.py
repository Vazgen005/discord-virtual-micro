import soundcard as sc
from soundcard.mediafoundation import _Speaker


def get_virtual(microphone: str | None) -> _Speaker | None:
    if not microphone or microphone == "default":
        microphone = "Virtual Cable"
    for i in sc.all_speakers():
        if microphone in i.name:
            return i
    return None


def get_physical(speaker: str | None) -> _Speaker | None:
    if not speaker or speaker == "default":
        return sc.default_speaker()
    for i in sc.all_speakers():
        if speaker in i.name:
            return i
    return None
