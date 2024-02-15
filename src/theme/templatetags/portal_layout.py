from django import template
from urllib.parse import urlencode , urlparse , urlunparse , parse_qs
from django.templatetags.static import static

from django.conf import settings

register = template.Library()

@register.simple_tag
def portal_css():
    color_header = f"--colour-header:{settings.PORTAL_COLOR_HEADER};" if settings.PORTAL_COLOR_HEADER else ""
    portal_css = f"""
:root {
    {color_header}
}
"""
    return portal_css