from django.contrib import admin
from . import models


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    list_filter = ("tags",)


@admin.register(models.Ingredient)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


admin.site.register(models.Tag)
admin.site.register(models.Favorite)
admin.site.register(models.Follow)
admin.site.register(models.Quantity)
admin.site.register(models.Purchase)
