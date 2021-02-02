from django.urls import path
from shoplist import views


urlpatterns = [
    path("", views.RecipeListView.as_view(), name="index"),
    path("create-recipe/", views.new_recipe, name="create-recipe"),
    # path("edit-recipe/<int:pk>/", views.edit_recipe, name="edit-recipe"),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipedetail'),
    path("recipes/<int:pk>/edit/", views.edit_recipe, name='edit-recipe'),
    # path("recipes/<int:pk>/edit/", views.RecipeUpdate.as_view(), name='edit-recipe'),
    path("recipes/<int:pk>/del/", views.del_recipe, name='recipedel'),
    path("favorites", views.api_favorite, name="add_favorite"),
    path("favorites/<int:pk>", views.del_favorite, name="del_favorite"),
    path("purchases", views.add_purchase, name="add_purchase"),
    path("purchases/<int:pk>", views.del_purchase, name="del_purchase"),
    path("shoplist/", views.PurchaseListView.as_view(), name="shoplist"),
    path("shoplist/get/", views.shoplist_generate, name="shoplist_generate"),
    path("subscriptions", views.add_follow, name="add_follow"),
    path("subscriptions/<str:author>", views.del_follow, name="del_follow"),
    # path("subscriptions/<int:pk>", views.del_follow_pk, name="del_follow_pk"),


    path("ingredients/", views.IngredientsApiView.as_view(), name="search_ingredients"),

    path("authorrecipe/", views.authorrecipe, name="authorrecipe"),
    path("changepassword/", views.changepassword, name="changepassword"),
    path("custompage/", views.custompage, name="custompage"),
    path("favorite/", views.FavoriteListView.as_view(), name="favorite"),
    path("formchangerecipe/", views.formchangerecipe, name="formchangerecipe"),
    # path("formrecipe/", views.formrecipe, name="formrecipe"),
    path("myfollow/", views.my_follow, name="myfollow"),
    path("reg/", views.reg, name="reg"),
    # path("resetpassword/", views.resetpassword, name="reset_password"),
    # path("shoplist/", views.shoplist, name="shoplist"),
    # path("singlepage/", views.singlepage, name="singlepage"),
    # path("singlepagenotauth/", views.singlepagenotauth, name="singlepagenotauth"),
]

