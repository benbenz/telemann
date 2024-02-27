from enum import Enum , StrEnum , IntEnum , auto 

class MIDIInterface(StrEnum):
    NONE = "---------"
    INTERNAL = "Internal MIDI"

class MIDIPattern(StrEnum):
    SUSTAINED_MIDDLE_C = "sustained middle C"
    SUSTAINED_LOW_C = "sustained low C"
    SUSTAINED_HIGH_C = "sustained high C"
    ARPEGGIATED_1 = "arpeggiated 1"

class MIDIRange(Enum):
    FULL = 1 , "Full"
    NATURAL = 2,"Natural"
    COMPACT = 3,"Compact"
    LOWER  = 4,"Lower"
    LOWER_EXTENDED = 6,"Lower+"
    HIGHER = 5,"Higher"
    HIGHER_EXTENDED = 7,"Higher+"
