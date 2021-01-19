from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from .models import Recipe
from django.urls import reverse_lazy
from . import forms


class RecipeListView(ListView):
    model = Recipe
    template_name = 'indexNotAuth.html'
    paginate_by = 6


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = forms.RecipeForm
    template_name = 'formRecipe.html'
    success_url = reverse_lazy('index')


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'singlePageNotAuth.html'



def auth(request):
    return render(
        request,
        'login.html'
    )


def authorrecipe(request):
    return render(
        request,
        'authorRecipe.html'
    )


def changepassword(request):
    return render(
        request,
        'password_change_form.html'
    )


def custompage(request):
    return render(
        request,
        'customPage.html'
    )


def favorite(request):
    return render(
        request,
        'favorite.html'
    )


def formchangerecipe(request):
    return render(
        request,
        'formChangeRecipe.html'
    )





def myfollow(request):
    return render(
        request,
        'myFollow.html'
    )


def reg(request):
    return render(
        request,
        'reg.html'
    )


def resetpassword(request):
    return render(
        request,
        'password_reset_form.html'
    )


def shoplist(request):
    return render(
        request,
        'shopList.html'
    )


def singlepage(request):
    return render(
        request,
        'singlePage.html'
    )



