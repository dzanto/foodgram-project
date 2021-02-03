from django import template
from shoplist.models import Purchase

register = template.Library()


@register.filter
def is_purch_by(recipe, user):
    return recipe.purchases.filter(user=user).exists()


