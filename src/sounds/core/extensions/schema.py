from typing import List , Optional , Tuple , Any
from abc import ABC , abstractmethod
from pydantic import BaseModel , confloat , conint
from .compositing.locale_en import sentences , words , cleanup
from .compositing.keys import * # import the k_*** keys
from .defs import *
import random
import math
import re

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

class Component(BaseModel,ABC):

    pass

class MixableComponent(Component):

    # we set Oscillators has MixedComponent for convenience purpose (to generate pre/post volume desc)
    # but we may want to have the default volume to None (when its actually not really used as a mixed component)
    volume : Optional[confloat(ge=0.0,le=1.0)]=None

class Mixer(Component): # SUM
    # re-type inputs
    inputs: Optional[List[MixableComponent]] = None

    def __iter__(self):
        for input in self.inputs:
            yield input

class Envelope(Component):

    attack : confloat(ge=0.0,le=1.0)
    decay  : confloat(ge=0.0,le=1.0)
    sustain: confloat(ge=0.0,le=1.0)
    release: confloat(ge=0.0,le=1.0)
    type   : EnvelopeType
    
class LFO(Component):

    waveform: WaveformEnum
    frequency : confloat(ge=0.0,le=1.0)
    delay : confloat(ge=0.0,le=1.0)

class OscillatorShape(MixableComponent):

    waveform : WaveformEnum
    width: WaveformWidthEnum|None = None
    
class Oscillator(MixableComponent):

    rank : conint(ge=1)
    shapes : List[OscillatorShape]=[]
    tune_coarse :  Optional[conint(multiple_of=12,ge=-24,le=24)]=None # = range = octave
    tune_fine : Optional[confloat(ge=-6.0,le=6.0)]=None
    detune : Optional[confloat(ge=0.0,le=1.0)]=None
    sub : bool=False
    sub_octave : Optional[conint(ge=-4,le=-1)]=None # [-4,-1] suboscillator octave range

class Operator(MixableComponent):

    type: Operation
    operands : Optional[List[ComponentID|Component]]=None
    bias : Optional[Any]=None

class Filter(MixableComponent):

    pass

class Amplifier(Component):

    volume: confloat(ge=0.0,le=1.0)

class Modulation(Component):

    source_id  : ModulationSourceID
    source     : Optional[Oscillator|LFO|Envelope]=None
    dest_id    : ModulationDestID
    dest       : Optional[Oscillator|Filter|LFO|Envelope]=None
    dest_param : ModulationDestParam
    depth      : float

class ModulationMatrix(Component):

    modulations : List[Modulation]=[]
    # pwm   : Optional[List[Modulation]]=None
    # pitch : Optional[List[Modulation]]=None
    # ring  : Optional[List[ModulationSource]]=None
    # cross : Optional[List[ModulationSource]]=None
    # sync  : Optional[List[ModulationSource]]=None

    def add_modulation(self,modulation:Modulation):
        self.modulations.append(modulation)

class Effect(Component):

    type : EffectType


class GlobalSettings(Component):
    
    detune : Optional[confloat(ge=0.0,le=1.0)]=None


# this is to handler Layers of SynthMaster
class Architecture(Component):

    # meta info ("Layer1")
    name : str 
    rank : conint(ge=1)
    type: ArchitectureType

    # common elements
    envelopes: Optional[List[Envelope]]=None 
    lfos: Optional[List[LFO]]=None
    mod_matrix: Optional[ModulationMatrix]=None

class SubtractiveArchitecture(Architecture):

    def __init__(self,**kwargs):
        super().__init__(type=ArchitectureType.SUBTRACTIVE,**kwargs)

    oscillators : Optional[List[Oscillator|Operator]|Mixer]=None
    filters: Optional[List[Filter]|Mixer]=None
    amplifier: Optional[Amplifier]=None

class SoundToneDescription(Component):

    architectures:Optional[List[Architecture]]=None
    effects: Optional[List[Effect]]=None
    settings: Optional[GlobalSettings]=None
