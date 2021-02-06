from django import template

from shoplist.models import Purchase

register = template.Library()


@register.filter
def is_purch_by(recipe, user):
    return Purchase.objects.filter(recipe=recipe, user=user).exists()


@register.filter
def set_tag_qs(request, tag):
    tags = request.GET.getlist('tag')
    if tag in tags:
        tags.remove(tag)
    else:
        tags.append(tag)
    for i in range(len(tags)):
        tags[i] = 'tag=' + tags[i]
    url_str = '&'.join(tags)
    return url_str


@register.filter
def parse_tags(request):
    tags = request.GET.getlist('tag')
    for i in range(len(tags)):
        tags[i] = 'tag=' + tags[i]
    url_str = '&'.join(tags)
    return url_str
