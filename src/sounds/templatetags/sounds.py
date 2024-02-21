from django import template
from urllib.parse import urlencode , urlparse , urlunparse , parse_qs
from django.templatetags.static import static
from ..models import SoundSource

register = template.Library()

MAX_LEN = 800

@register.filter(name="generator_type_icon")
def generator_type_icon(type):
    if type == SoundSource.Type.FILES.value:
        return "<i class=\"fa-solid fa-microphone\"></i>"
    elif type == SoundSource.Type.RECORDING.value:
        return "<i class=\"fa-solid fa-microphone\"></i>"
    elif type == SoundSource.Type.VOICE.value:
        return "<i class=\"fa-solid fa-microphone-lines\"></i>"
    elif type == SoundSource.Type.INSTRUMENT.value:
        return "<i class=\"fa-regular fa-piano-keyboard\"></i>"
    else:
        return "<i class=\"fa-solid fa-microphone\"></i>"
    
TAB = 0 

@register.simple_tag
def tab_index():
    global TAB
    res = TAB
    TAB +=1 
    return res

