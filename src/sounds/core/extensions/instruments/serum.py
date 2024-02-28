
from .base import InstrumentExtension
from pedalboard import AudioProcessorParameter, ExternalPlugin
from sounds.models import SoundSource 

class SerumExtension(InstrumentExtension):

    def generate_text(self,sound_info):
        return "not implemented"

    def arp_get(self, instrument)->float:
        pass

    def arp_set(self, instrument, value: float):
        pass

    def analyze_sound(self, source:SoundSource, instrument:ExternalPlugin, sound_info:dict):
        pass
