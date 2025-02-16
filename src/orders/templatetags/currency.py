from django import template

register = template.Library()


@register.filter
def rubles(value):
    try:
        return float(value) / 100
    except (ValueError, TypeError):
        return value
