from enum import StrEnum , IntFlag , IntEnum , auto

class WaveformEnum(StrEnum):
    SINE = auto()
    TRIANGLE = auto()
    TRISHAPED = auto()
    SQUARE = auto()
    PULSE = auto()
    PULSE_THIN = auto()
    SAWTOOTH = auto()
    SAWMULTI = auto()
    SAWUP = auto()
    SAWDOWN = auto()
    NOISE = auto()
    NOISE_WHITE = auto()
    NOISE_PINK = auto()
    SAMPLE = auto()
    ADDITIVE = auto()
    DIGITAL = auto()
    FBK_SAW = auto() # feedback saw (for Diva)
    EXOTIC = auto()
    S_H = auto()
    OTHER = auto()

class WaveformWidthEnum(StrEnum):
    NORMAL = auto()
    NARROW = auto()
    THIN = auto()
    WIDE = auto()
    VERY_WIDE = auto()
    SILENCE = auto() 

class ComponentID(StrEnum):
    ENV1 = "ENV1"
    ENV2 = auto() 
    ENV3 = auto() 
    ENV4 = auto()
    ENV5 = auto()
    ENV6 = auto()
    ENV7 = auto() 
    ENV8 = auto()
    ENV9 = auto()
    ENV10 = auto()
    LFO1 = auto() 
    LFO2 = auto() 
    LFO3 = auto() 
    LFO4 = auto() 
    LFO5 = auto() 
    LFO6 = auto() 
    LFO7 = auto() 
    LFO8 = auto() 
    LFO9 = auto() 
    LF10 = auto() 
    OSC1 = auto()
    OSC2 = auto()
    OSC3 = auto()
    OSC4 = auto()
    OSC5 = auto()
    OSC6 = auto()
    FILT1 = auto()
    FILT2 = auto()
    FILT3 = auto()
    FILT4 = auto()
    FILT5 = auto()
    FILT6 = auto()
    AMP  = auto()  

class ModulationSourceID(StrEnum):
    ENV1 = auto()
    ENV2 = auto() 
    ENV3 = auto() 
    ENV4 = auto()
    ENV5 = auto()
    ENV6 = auto()
    ENV7 = auto() 
    ENV8 = auto()
    ENV9 = auto()
    ENV10 = auto()
    LFO1 = auto() 
    LFO2 = auto() 
    LFO3 = auto() 
    LFO4 = auto() 
    LFO5 = auto() 
    LFO6 = auto() 
    LFO7 = auto() 
    LFO8 = auto() 
    LFO9 = auto() 
    LF10 = auto() 
    OSC1 = auto()
    OSC2 = auto()
    OSC3 = auto()
    OSC4 = auto()
    OSC5 = auto()
    OSC6 = auto()
    FILT1 = auto()
    FILT2 = auto()
    FILT3 = auto()
    FILT4 = auto()
    FILT5 = auto()
    FILT6 = auto()
    AMP  = auto()      
    KEYBOARD = auto()
    VELOCITY = auto()
    AFTERTOUCH = auto()
    OTHER = auto()

class ModulationDestID(StrEnum):
    ENV1 = auto()
    ENV2 = auto() 
    ENV3 = auto() 
    ENV4 = auto()
    ENV5 = auto()
    ENV6 = auto()
    ENV7 = auto() 
    ENV8 = auto()
    ENV9 = auto()
    ENV10 = auto()
    LFO1 = auto() 
    LFO2 = auto() 
    LFO3 = auto() 
    LFO4 = auto() 
    LFO5 = auto() 
    LFO6 = auto() 
    LFO7 = auto() 
    LFO8 = auto() 
    LFO9 = auto() 
    LF10 = auto() 
    OSC1 = auto()
    OSC2 = auto()
    OSC3 = auto()
    OSC4 = auto()
    OSC5 = auto()
    OSC6 = auto()
    FILT1 = auto()
    FILT2 = auto()
    FILT3 = auto()
    FILT4 = auto()
    FILT5 = auto()
    FILT6 = auto()
    AMP  = auto()      
    OTHER = auto()  

class ModulationDestParam(StrEnum):
    # OSC mods
    SIGNAL= auto() # = SIGNAL PATH = AMPLITUDE = RINGMOD = multiply of signal => value of signal1 modulates the ampliture of signal 2 (dest) => param = AMP
    PITCH = auto() 
    SHAPE = auto()
    PWM   = auto()
    FM    = auto()
    FM_AMOUNT = auto()
    CROSS_MOD = auto() # equivalent to FM but lets differentiate the vocabulary
    CROSS_MOD_AMOUNT = auto()  # equivalent to FM_AMOUNT but lets differentiate the vocabulary
    SYNC_SOFT = auto()
    SYNC_HARD = auto()
    # FILTER
    CUTOFF = auto()
    RESONANCE = auto()
    # ENVELOPE
    RATE = auto()
    # AMP
    VOLUME = auto()

class Operation(StrEnum):
    FM = auto()
    ADD = auto()
    SUBSTRACT = auto()
    RINGMOD = auto() # RINGMOD is MULTIPLY but we sematically differentiate it here to simplify text generation later on ...
    MULTIPLY = auto()
    FEEDBACK = auto() # for single input/operand identity with volume/feedback

class EnvelopeType(StrEnum):
    ADSR = auto()     
    AR = auto()
    GATE = auto()

class EffectType(StrEnum):
    DISTORTION = auto()     
    WAVESHAPER = auto()
    SATURATION = auto()
    OVERDRIVE = auto()
    TREMOLO = auto()
    AUTOPAN = auto()
    CHORUS = auto()
    FLANGER = auto()   
    PHASER = auto()    
    REVERB = auto()    
    DELAY = auto()   
    COMPRESSION = auto()
    OTHER = auto()


class ArchitectureType(StrEnum):
    SUBTRACTIVE = auto()

class StyleGuide(StrEnum):
    BASIC = auto()
    SUCCINT = auto()
    CONCISE = auto() 
    DETAILED = auto()
    SPECIFICATION = auto()

class DeclarationsMask(IntFlag):
    NONE = 0 
    OSC_VOLUME = auto() # means that the mix of oscillators has been declared (OSCs | OSC level)
    OSC_TUNING = auto() # means that the tining of oscillators has been declared (OSCs | OSC level)
    SHAPE_VOLUME = auto() # means that the level of the shapes has been declared (Shape level)
    ALL = OSC_VOLUME | OSC_TUNING | SHAPE_VOLUME

# to uniformize style accross entities/siblings
class DeclarationFlavour(IntFlag):
    NONE = 0
    #ARCHS
    ARCHS_SINGULAR = auto()
    ARCHS_PLURAL = auto()
    # OSCS
    OSCS_MIX_NONE = auto()
    OSCS_MIX_BALANCED = auto()
    OSCS_MIX_FORWARD = auto()
    OSCS_MIX_DEFAULT = auto()
    OSCS_TUNING_NONE = auto()
    OSCS_TUNING_AFTERWARDS = auto()
    # OSC
    OSC_VOLUME_NONE = auto()
    OSC_VOLUME_NUMBER = auto() # always POST
    OSC_VOLUME_TEXT_PRE = auto()
    OSC_VOLUME_TEXT_POST = auto()
    OSC_TUNING_PITCH = auto()
    OSC_TUNING_OCT = auto()
    OSC_TUNING_NONE = auto()
    OSC_OTHER_WITH_ID = auto()
    OSC_OTHER_FOR_OPERATOR = auto()
    

    # SHAPE
    SHAPE_VOLUME_NONE = auto()
    SHAPE_VOLUME_NUMBER = auto() # always POST and always NUMBER
    # Groups
    GRP_ARCHS_ALL = ARCHS_PLURAL | ARCHS_SINGULAR
    GRP_OSCS_MIX_PRESENT = OSCS_MIX_BALANCED | OSCS_MIX_FORWARD
    GRP_OSCS_MIX_ALL = OSCS_MIX_NONE | OSCS_MIX_DEFAULT | GRP_OSCS_MIX_PRESENT
    GRP_OSCS_TUNING_PRESENT = OSCS_TUNING_AFTERWARDS
    GRP_OSCS_TUNING_ALL = GRP_OSCS_TUNING_PRESENT | OSCS_TUNING_NONE 
    GRP_OSC_VOLUME_PRESENT = OSC_VOLUME_NUMBER | OSC_VOLUME_TEXT_PRE | OSC_VOLUME_TEXT_POST
    GRP_OSC_VOLUME_ALL = OSC_VOLUME_NONE | GRP_OSC_VOLUME_PRESENT
    GRP_OSC_OTHER = OSC_OTHER_WITH_ID | OSC_OTHER_FOR_OPERATOR
    GRP_OSC_TUNING_PRESENT = OSC_TUNING_OCT | OSC_TUNING_PITCH
    GRP_OSC_TUNING_ALL = OSC_TUNING_NONE | GRP_OSC_TUNING_PRESENT
    GRP_SHAPE_VOLUME_PRESENT = SHAPE_VOLUME_NUMBER
    GRP_SHAPE_VOLUME_ALL = SHAPE_VOLUME_NONE | GRP_SHAPE_VOLUME_PRESENT
    # ALL 
    ALL = NONE | GRP_SHAPE_VOLUME_ALL | GRP_OSC_OTHER | GRP_OSC_VOLUME_ALL | GRP_OSC_TUNING_ALL | GRP_OSCS_MIX_ALL | GRP_OSCS_TUNING_ALL | GRP_ARCHS_ALL