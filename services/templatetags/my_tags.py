from django import template

register = template.Library()

@register.filter(name='star_range')
def star_range(value):
    return range(value)
