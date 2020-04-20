from django import template
import django.utils.html as utils
from django.utils import dateparse, timezone
import json
import pytz
register = template.Library()

#Helper methods for templates. Syntax in templates is using | with function name
@register.filter
def get_index(indexable, i):
    return indexable[i]

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)

@register.filter
def sort(lst):
    return sorted(lst)

@register.filter
def makeList(the_string):
    lst = json.loads(the_string)
    return lst

@register.filter
def toDate(timestamp):
    date = dateparse.parse_datetime(timestamp)
    return date
