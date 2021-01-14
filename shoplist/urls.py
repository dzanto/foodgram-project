from django.urls import path
from shoplist import views

urlpatterns = [
    path("", views.index, name="index"),
]