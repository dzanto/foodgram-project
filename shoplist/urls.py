from django.urls import path
from shoplist import views


urlpatterns = [
    path("", views.RecipeListView.as_view(), name="index"),
    path("create-recipe/", views.new_recipe, name="create-recipe"),
    # path("create-recipe/", views.RecipeCreateView.as_view(), name="create-recipe"),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipedetail'),
    path("favorites", views.api_favorite, name="add_favorite"),
    path("favorites/<int:pk>", views.del_favorite, name="del_favorite"),
    path("purchases", views.add_purchase, name="add_purchase"),
    path("purchases/<int:pk>", views.del_purchase, name="del_purchase"),

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
    path("shoplist/", views.shoplist, name="shoplist"),
    # path("singlepage/", views.singlepage, name="singlepage"),
    # path("singlepagenotauth/", views.singlepagenotauth, name="singlepagenotauth"),
]

