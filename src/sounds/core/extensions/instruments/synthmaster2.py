
from .base import InstrumentExtension
from pedalboard import AudioProcessorParameter, ExternalPlugin
from sounds.models import SoundSource 
from sounds.core.extensions.schema import SoundToneDescription
from typing import List,Optional

class SynthMaster2Extension(InstrumentExtension):

    def arp_disable(self, instrument):
        """ Implement me! """
        pass

    def arp_enable(self, instrument):
        """ Implement me! """
        pass

    def arp_is_on(self, instrument)->bool:  
        pass   

    def analyze_sound(self,parameters:dict) -> Optional[SoundToneDescription]:
        """ Implement me! """
        pass
