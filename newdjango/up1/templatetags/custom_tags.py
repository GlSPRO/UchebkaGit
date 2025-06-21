from django import template
import builtins

register = template.Library()

@register.filter(name='getattr')
def getattr_filter(obj, attr_name):
    return builtins.getattr(obj, attr_name, '')
