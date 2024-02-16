import mido
from enum import StrEnum , auto


class MIDIInterface(StrEnum):
    NONE = "---------"
    INTERNAL = "Internal MIDI"

def get_midi_output_ports():
    devices = mido.get_output_names()
    result = list()
    result.extend([
        (-2,MIDIInterface.NONE),
        (-1,MIDIInterface.INTERNAL)
    ])
    for idx,device in enumerate(devices):
        result.append(
            (idx,device)
        )
    return result 

def get_midi_input_ports():
    devices = mido.get_input_names()
    result = list()
    result.extend([
        (-2,MIDIInterface.NONE),
        (-1,MIDIInterface.INTERNAL)
    ])
    for idx,device in enumerate(devices):
        result.append(
            (idx,device)
        )
    return result 