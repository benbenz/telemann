import abc
from pedalboard import AudioProcessorParameter , ExternalPlugin
from sounds.models import SoundSource 
from enum import StrEnum , auto

class OscShape(StrEnum):
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
    SAMPLE = auto()
    ADDITIVE = auto()
    DIGITAL = auto()
    FEEDBACK = auto()
    EXOTIC = auto()
    OTHER = auto()

class InstrumentExtension(abc.ABC):

    @abc.abstractmethod
    def generate_text(self,sound_info):
        """ Implement me! """
        pass

    @abc.abstractmethod
    def arp_get(self, instrument)->float:
        """ Implement me! """
        pass

    @abc.abstractmethod
    def arp_set(self, instrument, value: float):
        """ Implement me! """
        pass

    """
    This should add the field analysis in sound_info and add the following sections:

    oscs: [
            { shapes : [ 'square'|'triangle'|'sine'|'pwm'|'saw'|'sawup'|'sawdown'|'sample'|'additive'|'digital'|'other', ...] , mix: 0.0...1.0 , sub: true|false, pwm: true|false } ,
            { shapes : ['square'|'triangle'|'sine'|'pwm'|'saw'|'sawup'|'sawdown'|'sample'|'additive'|'digital'|'other', ...] , mix: 0.0...1.0 , sub: true|false, pwm: true|false } ,
            ...
    ] ,
    filters : [
        { type : 'lowpass'|'highpass'|'bandpass'|'other' , slope: '6dB'|'12dB'|'18dB'|'24dB'... } ,
        { type : 'lowpass'|'highpass'|'bandpass'|'other' , slope: '6dB'|'12dB'|'18dB'|'24dB'... } ,
        ...        
    ] ,
    envs: { 
        { attack: 'fast'|'medium'|'slow' , release: 'fast'|'medium'|'slow' , sustain: 'low'|'medium'|'high' , decay:'slow'|'medium'|'fast'} ,
        { attack: 'fast'|'medium'|'slow' , release: 'fast'|'medium'|'slow' , sustain: 'low'|'medium'|'high' , decay:'slow'|'medium'|'fast'} ,
        ...
    } ,
    modulation: {
        cross_modulation: true|false,
        ring_modulation: 0.0....1.0,
        sync: true|false,
        pitch_env: 0.0...1.0
        pitch_lfo: 0.0...1.0
        filter_env: 0.0...1.0
        filter_lfo: 0.0...1.0
        amp_env: 0.0...1.0
        amp_lfo: 0.0...1.0
    }
    """
    @abc.abstractmethod
    def analyze_sound(self, source:SoundSource, instrument:ExternalPlugin, sound_info:dict):
        """ Implement me! """
        pass
    
