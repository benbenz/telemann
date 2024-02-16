from sounddevice import query_devices

from enum import StrEnum , auto

class AudioInterface(StrEnum):
    NONE = "---------"
    INTERNAL_CAPTURE = "Internal Capture"

def get_audio_input_interfaces():
    devices = query_devices()
    result = list()
    result.extend([
        (None,AudioInterface.NONE),
        (AudioInterface.INTERNAL_CAPTURE,AudioInterface.INTERNAL_CAPTURE)
    ])
    for device in devices:
        # this is an input
        if device['max_input_channels']>0:
            result.append(
                (device['name'],device['name'])
            )
    return result 
