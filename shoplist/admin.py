from django.contrib import admin

from django import forms

from . import models


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "show_count")
    search_fields = ("title", "author__username",)
    list_filter = ("tags",)

    def show_count(self, obj):
        result = models.Favorite.objects.filter(recipe=obj).count()
        return result

    show_count.short_description = "В избранном"


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("title", "dimension")
    search_fields = ("title",)


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user")
    search_fields = ("recipe__title", "user__username")


@admin.register(models.Quantity)
class QuantityAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "quantity")
    search_fields = ("ingredient__title", "recipe__title")


@admin.register(models.Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("author", "user")
    search_fields = ("author__username", "user__username")


@admin.register(models.Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user")
    search_fields = ("recipe__title", "user__username")


admin.site.register(models.Tag)
