import abc
import random
from pedalboard import AudioProcessorParameter , ExternalPlugin
from sounds.models import SoundSource 
from enum import StrEnum , auto
from typing import List , Optional
from ..schema import SoundToneDescription , StyleGuide
from ..compositing.descriptor import Descriptor

class InstrumentExtension(abc.ABC):

    @abc.abstractmethod
    def arp_get(self, instrument)->float|List[float]:
        """ Implement me! """
        pass

    @abc.abstractmethod
    def arp_set(self, instrument, value: float|List[float]):
        """ Implement me! """
        pass

    @abc.abstractmethod
    def arp_disable(self, instrument):
        """ Implement me! """
        pass

    @abc.abstractmethod
    def arp_is_on(self, instrument)->bool:  
        pass   

    @abc.abstractmethod
    def analyze_sound(self,parameters:dict) -> Optional[SoundToneDescription]:
        """ Implement me! """
        pass

    def describe_sound(self, description:Optional[SoundToneDescription], style_guide:Optional[StyleGuide]=None):
        
        if style_guide is None:
            style_guide = random.choice(list(StyleGuide))

        if description:
            descriptor = Descriptor()
            desc , _ , _ = descriptor.desc(description,style_guide)
            return desc
        else:
            return "No description available"
    
