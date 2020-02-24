from django import template
import django.utils.html as utils
import json
register = template.Library()

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
