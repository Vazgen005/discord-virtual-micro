import sys
import soundcard as sc

if sys.platform == "win32":
    from soundcard.mediafoundation import _Speaker
elif sys.platform == "linux":
    from soundcard.pulseaudio import _Speaker
else:
    raise NotImplementedError("SoundCard does not support {} yet".format(sys.platform))


def get_virtual(microphone: str | None) -> _Speaker | None:
    if not microphone or microphone == "default":
        microphone = "Virtual Cable"
    print("Searching for microphone...")
    for i in sc.all_speakers():
        if microphone in i.name:
            print("Founded microphone:", i.name)
            return i
        print("   ", i.name)
    return None


def get_physical(speaker: str | None) -> _Speaker | None:
    if not speaker or speaker == "default":
        return sc.default_speaker()
    for i in sc.all_speakers():
        if speaker in i.name:
            return i
    return None
