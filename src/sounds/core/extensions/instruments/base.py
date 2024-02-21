import abc
from pedalboard import AudioProcessorParameter , ExternalPlugin
from sounds.models import SoundSource 
from enum import StrEnum , auto

class OscShape(StrEnum):
    SINE = auto()
    TRIANGLE = auto()
    SQUARE = auto()
    PULSE = auto()
    PULSE_THIN = auto()
    SAWTOOTH = auto()
    SAWUP = auto()
    SAWDOWN = auto()
    NOISE = auto()
    SAMPLE = auto()
    ADDITIVE = auto()
    DIGITAL = auto()
    EXOTIC = auto()
    OTHER = auto()

class InstrumentExtension(abc.ABC):

    @abc.abstractmethod
    def generate_text(self,sound_info):
        """ Implement me! """
        pass

    @abc.abstractmethod
    def arp_off(self, instrument)->float:
        """ Implement me! """
        pass

    @abc.abstractmethod
    def arp_set(self, instrument, value: float):
        """ Implement me! """
        pass

    """
    This should add the field analysis in sound_info and add the following sections:

    oscs: [
            { shapes : [ 'square'|'triangle'|'sine'|'pwm'|'saw'|'sawup'|'sawdown'|'sample'|'additive'|'digital'|'other', ...] , mix: 0.0...1.0 } ,
            { shapes : ['square'|'triangle'|'sine'|'pwm'|'saw'|'sawup'|'sawdown'|'sample'|'additive'|'digital'|'other', ...] , mix: 0.0...1.0 } ,
            ...
    ] ,
    filters : [
        { type : 'lowpass'|'highpass'|'bandpass'|'other' , slope: '6dB'|'12dB'|'18dB'|'24dB'... } ,
        { type : 'lowpass'|'highpass'|'bandpass'|'other' , slope: '6dB'|'12dB'|'18dB'|'24dB'... } ,
        ...        
    ] ,
    envs: { 
        amp: { attack: 'fast'|'medium'|'slow' , release: 'fast'|'medium'|'slow' , sustain: 'low'|'medium'|'high' , decay:'slow'|'medium'|'fast'} ,
        filter: { attack: 'fast'|'medium'|'slow' , release: 'fast'|'medium'|'slow' , sustain: 'low'|'medium'|'high', decay:'slow'|'medium'|'fast'} ,
    } ,
    modulation: {
        cross_modulation: true|false,
        ring_modulation: true|false,
        pwm: true|false,
        sync: true|false,
        pitch_env: 'strong'|'light'
    }
    """
    @abc.abstractmethod
    def analyze_sound(self, source:SoundSource, instrument:ExternalPlugin, sound_info:dict):
        """ Implement me! """
        pass
    
