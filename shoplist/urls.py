from django.urls import path
from shoplist import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", views.RecipeListView.as_view(), name="index"),
    path("formrecipe/", views.RecipeCreateView.as_view(), name="formrecipe"),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipedetail'),
    # path("favorites/", views.recipe_add_favorite, name="add_favorite"),
    path("favorites", csrf_exempt(views.APIFavorite.as_view()), name="addfavorite"),
    # path("auth/", views.auth, name="auth"),
    path("authorrecipe/", views.authorrecipe, name="authorrecipe"),
    path("changepassword/", views.changepassword, name="changepassword"),
    path("custompage/", views.custompage, name="custompage"),
    path("favorite/", views.favorite, name="favorite"),
    path("formchangerecipe/", views.formchangerecipe, name="formchangerecipe"),
    # path("formrecipe/", views.formrecipe, name="formrecipe"),
    path("myfollow/", views.myfollow, name="myfollow"),
    path("reg/", views.reg, name="reg"),
    # path("resetpassword/", views.resetpassword, name="reset_password"),
    path("shoplist/", views.shoplist, name="shoplist"),
    # path("singlepage/", views.singlepage, name="singlepage"),
    # path("singlepagenotauth/", views.singlepagenotauth, name="singlepagenotauth"),
]

