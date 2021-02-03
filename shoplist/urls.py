from django.urls import path
from shoplist import views


urlpatterns = [
    path("", views.RecipeListView.as_view(), name="index"),
    path("create-recipe/", views.new_recipe, name="create-recipe"),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipedetail'),
    path("recipes/<int:pk>/edit/", views.edit_recipe, name='edit-recipe'),
    path("recipes/<int:pk>/del/", views.del_recipe, name='recipedel'),
    path("favorites", views.api_favorite, name="add_favorite"),
    path("favorites/<int:pk>", views.del_favorite, name="del_favorite"),
    path("purchases", views.add_purchase, name="add_purchase"),
    path("purchases/<int:pk>", views.del_purchase, name="del_purchase"),
    path("shoplist/", views.PurchaseListView.as_view(), name="shoplist"),
    path("shoplist/get/", views.shoplist_generate, name="shoplist_generate"),
    path("subscriptions", views.add_follow, name="add_follow"),
    path("subscriptions/<str:author>", views.del_follow, name="del_follow"),
    path("ingredients/", views.IngredientsApiView.as_view(), name="search_ingredients"),
    path("recipes/<str:author>", views.recipe_list, name="authorrecipes"),
    path("favorite/", views.FavoriteListView.as_view(), name="favorite"),
    path("myfollow/", views.my_follow, name="myfollow"),
]
