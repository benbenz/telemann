from django import template
from urllib.parse import urlencode , urlparse , urlunparse , parse_qs
from django.templatetags.static import static
from ..models import SoundGenerator

register = template.Library()

MAX_LEN = 800

@register.filter(name="generator_type_icon")
def source_ellipsis(type):
    if type == SoundGenerator.Type.RECORDING.value:
        return "<i class=\"fa-solid fa-microphone\"></i>"
    elif type == SoundGenerator.Type.AUDIOFILES.value:
        return "<i class=\"fa-solid fa-file-audio\"></i>"
    elif type == SoundGenerator.Type.ARTIST.value:
        return "<i class=\"fa-solid fa-microphone-lines\"></i>"
    elif type == SoundGenerator.Type.INSTRUMENT.value:
        return "<i class=\"fa-regular fa-piano-keyboard\"></i>"
    else:
        return "<i class=\"fa-solid fa-microphone\"></i>"

