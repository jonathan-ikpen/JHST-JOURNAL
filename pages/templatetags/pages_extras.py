from django import template

register = template.Library()


@register.filter
def splitlines(value):
    """Split a newline-delimited string into a list of non-empty lines."""
    if not value:
        return []
    return [line.strip() for line in value.splitlines() if line.strip()]


@register.filter
def split_colon(value):
    """Split a string by the first colon and return a list of two parts."""
    if not value or ':' not in value:
        return [value, ""]
    parts = value.split(':', 1)
    return [parts[0].strip(), parts[1].strip()]
