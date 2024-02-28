from typing import List , Optional
from enum import StrEnum , auto
from abc import ABC , abstractmethod
from pydantic import BaseModel , confloat

class OscillatorShapeEnum(StrEnum):
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

class ModulationSourceEnum(StrEnum):
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
    OTHER = auto()

class StyleGuide(StrEnum):
    ESSENTIALS = auto()
    ULTRA_COMPACT = auto() 
    COMPACT = auto() 
    OMITTED = auto()
    DETAILED = auto()
    FULL = auto()

class ExtensionComponent(BaseModel,ABC):

    @abstractmethod
    def desc(self,style_guide:StyleGuide)->Optional[str]:
        pass

class ModulationSource(ExtensionComponent):

    source : ModulationSourceEnum 
    level : confloat(gt=0.0,lt=1.0)

    def desc(self,style_guide:StyleGuide)->Optional[str]:
        return None
    
class ModulationSources(ExtensionComponent):
    
    sources : List[ModulationSource]=[]

    def desc(self,style_guide:StyleGuide)->Optional[str]:
        return None
    
    def add(self,modulation_source:ModulationSource):
        self.sources.append(modulation_source)
    
class OscModulationMatrix(ExtensionComponent):

    pwm : Optional[ModulationSources]=None
    pitch : Optional[ModulationSources]=None

    def desc(self,style_guide:StyleGuide)->Optional[str]:
        return None

class OscillatorShape(ExtensionComponent):

    shape : OscillatorShapeEnum

    def desc(self,style_guide:StyleGuide)->Optional[str]:
        return None
    
class Oscillator(ExtensionComponent):

    shapes : List[OscillatorShape]=[]
    volume : confloat(gt=0.0,lt=1.0)
    sub : bool 
    mod : Optional[OscModulationMatrix]=None

    def desc(self,style_guide:StyleGuide)->Optional[str]:
        return None
    
class SoundToneDescription(ExtensionComponent):

    oscillators: List[Oscillator]=[] 

    def desc(self,style_guide:StyleGuide)->Optional[str]:
        return None



