from django import template

from shoplist.models import Purchase

register = template.Library()


@register.filter
def is_purch_by(recipe, user):
    return Purchase.objects.filter(recipe=recipe, user=user).exists()


@register.filter
def set_tag_qs(request, tag):
    pass
