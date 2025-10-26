# habit_app/templatetags/dict_extras.py

from django import template

# Register the template library
register = template.Library()

# Custom filter to get a value from a dictionary by key
@register.filter
def dict_get(d, key):
    """
    Usage in template:
    {{ your_dict|dict_get:key }}

    Returns the value for the given key in the dictionary `d`.
    """
    if d is None:
        return None
    return d.get(key)
