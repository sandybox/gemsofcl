from django.conf import settings
from django import template
#from django.template.defaultfilters import floatformat

import logging
logger = logging.getLogger(__name__)

register = template.Library()

@register.filter
def percent(value):
    if value is None:
        return None
    return str(int(value * 100)) + '%'

@register.filter
def trimtitle(text):
    r = text.rfind("-")
    if r != -1:
        return text[:r]
    return text
