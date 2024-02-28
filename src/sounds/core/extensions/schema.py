from typing import List , Optional
from enum import StrEnum , auto
from abc import ABC , abstractmethod
from pydantic import BaseModel , confloat
from .compositing_en import sentences
import random

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
    BASIC = auto()
    SUCCINT = auto()
    CONCISE = auto() 
    DETAILED = auto()

class ExtensionComponent(BaseModel,ABC):

    @abstractmethod
    def desc(self,style_guide:StyleGuide)->Optional[str]:
        pass

class ModulationSource(ExtensionComponent):

    source : ModulationSourceEnum 
    level : confloat(ge=0.0,le=1.0)

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
    volume : confloat(ge=0.0,le=1.0)
    sub : bool 
    mod : Optional[OscModulationMatrix]=None

    def desc(self,style_guide:StyleGuide)->Optional[str]:
        return "an oscillator"
    
class SoundToneDescription(ExtensionComponent):

    oscillators: List[Oscillator]=[] 

    def desc(self,style_guide:StyleGuide)->Optional[str]:

        osc_desc = self._desc_oscillators(style_guide=style_guide)

        return osc_desc
    
    def _is_osc_mix_balanced(self):
        if self.oscillators is None or len(self.oscillators)==1:
            return False
        vol_total = 0.0
        for osc in self.oscillators:
            vol_total += osc.volume

        if vol_total==0.0:
            return True
        vol_avg = vol_total / len(self.oscillators)

        for osc in self.oscillators:
            if osc.volume > vol_avg * 1.2 or osc.volume < vol_avg * 0.8 :
                return False
            
        return True


    def _desc_oscillators(self,style_guide:StyleGuide)->Optional[str]:
        if self.oscillators is None or len(self.oscillators)==0:
            return None
        
        oscillators_descs : List = [osc.desc(style_guide) for osc in self.oscillators]

        sentences_osc = sentences['oscillators']

        glue = random.choice( sentences_osc["glue"][style_guide.value] )

        oscillators_desc_inner = glue.join(oscillators_descs)

        plurality = "plural" if len(oscillators_descs)>1 else "singular"

        balanced_mix = self._is_osc_mix_balanced()

        if balanced_mix is True:
            compositing_choices = sentences_osc["compositing"][style_guide.value][plurality] + sentences_osc["compositing"][style_guide.value]["balanced"]
        else:
            compositing_choices = sentences_osc["compositing"][style_guide.value][plurality]
        
        compositing = random.choice( compositing_choices )
        
        oscillators_desc = compositing.format(oscillators_desc=oscillators_desc_inner)

        return oscillators_desc





