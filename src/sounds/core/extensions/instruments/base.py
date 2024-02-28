import abc
import random
from pedalboard import AudioProcessorParameter , ExternalPlugin
from sounds.models import SoundSource 
from enum import StrEnum , auto
from typing import List , Optional
from ..schema import SoundToneDescription , StyleGuide

class InstrumentExtension(abc.ABC):

    @abc.abstractmethod
    def arp_get(self, instrument)->List|float:
        """ Implement me! """
        pass

    @abc.abstractmethod
    def arp_set(self, instrument, value: List|float):
        """ Implement me! """
        pass

    @abc.abstractmethod
    def arp_disable(self, instrument):
        """ Implement me! """
        pass

    @abc.abstractmethod
    def arp_is_on(self, instrument)->bool:  
        pass   

    """
    This should add the field analysis in sound_info and add the following sections:

    oscs: [
            { shapes : [ 'square'|'triangle'|'sine'|'pwm'|'saw'|'sawup'|'sawdown'|'sample'|'additive'|'digital'|'other'|'sub', ...] , mix: 0.0...1.0 , pwm: true|false } ,
            { shapes : ['square'|'triangle'|'sine'|'pwm'|'saw'|'sawup'|'sawdown'|'sample'|'additive'|'digital'|'other'|'sub', ...] , mix: 0.0...1.0 , pwm: true|false } ,
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
    def analyze_sound(self,parameters:dict) -> Optional[SoundToneDescription]:
        """ Implement me! """
        pass

    def describe_sound(self, description:Optional[SoundToneDescription], style_guide:Optional[StyleGuide]=None):
        
        if style_guide is None:
            style_guide = random.choice(list(StyleGuide))

        if description:
            return description.desc(style_guide)
        else:
            return "No description available"
    
