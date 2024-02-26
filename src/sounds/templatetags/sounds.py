from django import template
from urllib.parse import urlencode , urlparse , urlunparse , parse_qs
from django.templatetags.static import static
from ..models import SoundSource

register = template.Library()

MAX_LEN = 800

@register.filter(name="source_type_icon")
def source_type_icon(type):
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
    
@register.filter(name="source_plugin_icon")
def source_plugin_icon(source):
    if source.file_path is None:
        return ""
    src = None
    if source.file_path.endswith('.component'):
        src = 'audio_unit.png'
    elif source.file_path.endswith('.vst3'):
        src = 'VST3.png'
    elif source.file_path.endswith('.vst'):
        src = 'VST.png'
    if src is None:
        return ""
    src = static(f"images/logos/{src}")
    return f"<img src=\"{src}\" class=\"source-plugin-icon\"/>"
    
TAB = 0 

@register.simple_tag
def tab_index():
    global TAB
    res = TAB
    TAB +=1 
    return res



