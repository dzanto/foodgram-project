from django.urls import path
from shoplist import views


urlpatterns = [
    path('', views.RecipeListView.as_view(), name='index'),
    path('create-recipe/', views.new_recipe, name='create-recipe'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(),
         name='recipedetail'),
    path('recipes/<int:pk>/edit/', views.edit_recipe, name='edit-recipe'),
    path('recipes/<int:pk>/del/', views.del_recipe, name='recipedel'),
    path('shoplist/', views.PurchaseListView.as_view(), name='shoplist'),
    path('shoplist/get/', views.shoplist_generate, name='shoplist_generate'),
    path('recipes/<str:author>', views.authors_recipes, name='authorrecipes'),
    path('favorite/', views.FavoriteListView.as_view(), name='favorite'),
    path('myfollow/', views.my_follow, name='myfollow'),

    path('about/', views.about, name='about'),
    path('features/', views.features, name='features'),

    path('api/favorites/', views.api_favorite, name='add_favorite'),
    path('api/favorites/<int:pk>/', views.del_favorite, name='del_favorite'),
    path('api/purchases/', views.add_purchase, name='add_purchase'),
    path('api/purchases/<int:pk>/', views.del_purchase, name='del_purchase'),
    path('api/subscriptions/', views.add_follow, name='add_follow'),
    path('api/subscriptions/<str:author>/', views.del_follow,
         name='del_follow'),
    path('api/ingredients/', views.IngredientsApiView.as_view(),
         name='search_ingredients'),
]
