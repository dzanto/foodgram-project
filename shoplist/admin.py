from django.contrib import admin
from .models import Ingredient, Recipe


# class ShoplistAdmin(admin.ModelAdmin):
#     list_display = ("text", "pub_date", "author")
#     search_fields = ("text",)
#     list_filter = ("pub_date",)
#     empty_value_display = "-пусто-"


admin.site.register(Ingredient)
admin.site.register(Recipe)

