from django import template

register = template.Library()

@register.filter
def to_char(value):
    return chr(96+value)

@register.filter
def percentage_to_decimal(value):
    print value
    return str(round(int(value)/100.0, 2))
