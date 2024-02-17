import random
from django import template
import uuid 

register = template.Library()

@register.simple_tag
def random_uuid():
    return uuid.uuid4().hex
