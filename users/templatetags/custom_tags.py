# custom_tags.py
from django import template

register = template.Library()

@register.filter(name='is_customer')
def is_customer(value):
    if value is None:
        return False
    return value.lower() == 'customer'

@register.filter(name='is_seller')
def is_seller(value):
    if value is None:
        return False
    return value.lower() == 'seller'
  
@register.filter(name='is_admin')
def is_admin(value):
    if value is None:
        return False
    return value.lower() == 'admin'
