from django import template
from .models import Purchase

register = template.Library()


@register.filter
def is_purch_by(recipe, user):
    # return Purchase.objects.filter(user=user, recipe=recipe).exists()
    return recipe.purchases.filter(user=user).exists()
