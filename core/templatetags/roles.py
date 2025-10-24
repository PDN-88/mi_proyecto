from django import template
register = template.Library()

@register.filter
def in_group(user, group_name):
    # ahora no importa si pones "Inquilinos", "inquilinos", etc.
    return user.is_authenticated and user.groups.filter(name__iexact=group_name).exists()