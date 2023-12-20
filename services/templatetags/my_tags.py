from django import template

register = template.Library()

@register.filter(name='star_range')
def star_range(value):
    return range(value)

@register.filter(name='full_stars')
def full_stars(value):
    return range(int(value))

@register.filter(name='half_star')
def half_star(value):
    return 1 if value - int(value) >= 0.5 else 0

@register.filter(name='empty_stars')
def empty_stars(value):
    return range(5 - int(value) - half_star(value))
