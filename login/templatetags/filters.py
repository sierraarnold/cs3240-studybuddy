from django import template
register = template.Library()

@register.filter
def get_index(indexable, i):
    return indexable[i]

@register.filter
def sort(lst, key_name):
    return sorted(lst)

@register.filter
def makeList(the_string, key_name):
    strs = the_string.replace('[','').split('],')
    lst = [map(str, s.replace(']','').split(',')) for s in strs]
    for (i, map_object) in enumerate(lst):
        lst[i] = list(map_object)
        for (j, item) in enumerate(lst[i]):
            lst[i][j] = item.replace('"', '')
    return lst
