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


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user")
    search_fields = ("recipe", "user")


@admin.register(models.Quantity)
class QuantityAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "quantity")
    search_fields = ("ingredient", "recipe")


@admin.register(models.Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("author", "user")
    search_fields = ("author", "user")


@admin.register(models.Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user")
    search_fields = ("recipe", "user")


admin.site.register(models.Tag)
