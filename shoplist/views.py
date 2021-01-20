from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from .models import Recipe, User, Favorite
from django.urls import reverse_lazy
from . import forms, serializers
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics


class RecipeListView(ListView):
    model = Recipe
    template_name = 'indexNotAuth.html'
    paginate_by = 6


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = forms.RecipeForm
    template_name = 'formRecipe.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        task = form.save(commit=False)
        task.author = self.request.user
        task.save()
        return super().form_valid(form)


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'singlePage.html'


# @login_required
# def profile_follow(request, username):
#
#     author = get_object_or_404(User, username=username)
#
#     if author == request.user:
#         return redirect("profile", username=username)
#
#     following = Follow.objects.filter(user=request.user).filter(author=author).exists()
#     if following:
#         return redirect("profile", username=username)
#
#     follow = Follow()
#     follow.author = author
#     follow.user = request.user
#     follow.save()
#     return redirect("profile", username=username)


@login_required
def recipe_add_favorite(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    is_favorite = Favorite.objects.filter(user=request.user).filter(recipe=recipe).exists()
    if is_favorite:
        return redirect("recipedetail", pk=pk)
    favorite = Favorite()
    favorite.recipe = recipe
    favorite.user = request.user
    favorite.save()
    return redirect("recipedetail", pk=pk)


class APIFavorite(APIView):

    def post(self, request):
        id = int(request.data['id'])
        recipe = get_object_or_404(Recipe, id=id)
        data = {'user': request.user.id, 'recipe': id}
        serializer = serializers.FavoriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response(request.data)




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



