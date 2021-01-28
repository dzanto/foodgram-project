from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from .models import Recipe, User, Favorite, Follow, Ingredient, Quantity
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
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import filters
from django.core.paginator import Paginator


class RecipeListView(ListView):
    model = Recipe
    template_name = 'indexNotAuth.html'
    paginate_by = 3


def new_recipe(request):

    if request.method != "POST":
        form = forms.RecipeForm()
        return render(request, "formRecipe.html", {"form": form})

    form = forms.RecipeForm(request.POST, request.FILES)
    if not form.is_valid():
        for field in request.POST:
            print(field)
        return render(request, "formRecipe.html",
                      {"form": form})

    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    for field in request.POST:
        print(field)
        # 'nameIngredient_1': ['молоко 4%'], 'valueIngredient_1': ['4'],
        if 'nameIngredient' in field:
            name_ingredient = request.POST[field]
            value_ingredient = int(request.POST[field.replace('name', 'value')])
            print(name_ingredient, value_ingredient)
            ingredient = Ingredient.objects.get(title=name_ingredient)
            quantity = Quantity.objects.create(
                ingredient=ingredient,
                recipe=recipe,
                quantity=value_ingredient
            )
    return redirect("index")


# class RecipeCreateView(CreateView):
#     model = Recipe
#     form_class = forms.RecipeForm
#     template_name = 'formRecipe.html'
#     success_url = reverse_lazy('index')
#
#     def form_valid(self, form):
#         task = form.save(commit=False)
#         task.author = self.request.user
#         task.save()
#         return super().form_valid(form)


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'singlePage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_anonymous:
            return context
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        context['favorite'] = Favorite.objects.filter(
            recipe_id=recipe.id).filter(
            user=self.request.user).exists()
        return context


class FavoriteListView(ListView):
    model = Recipe
    template_name = 'favorite.html'
    paginate_by = 3

    def get_queryset(self):
        recipes = Recipe.objects.filter(favorites__user=self.request.user)
        return recipes


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


# @login_required
# def recipe_add_favorite(request, pk):
#     recipe = get_object_or_404(Recipe, id=pk)
#     is_favorite = Favorite.objects.filter(user=request.user).filter(recipe=recipe).exists()
#     if is_favorite:
#         return redirect("recipedetail", pk=pk)
#     favorite = Favorite()
#     favorite.recipe = recipe
#     favorite.user = request.user
#     favorite.save()
#     return redirect("recipedetail", pk=pk)


# class APIFavorite(APIView):
#
#     def post(self, request):
#         id = int(request.data['id'])
#         print(id)
#         print(request.user)
#         recipe = get_object_or_404(Recipe, id=id)
#         data = {'user': request.user.id, 'recipe': id}
#         serializer = serializers.FavoriteSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
@api_view(['POST'])
def api_favorite(request):
    id = int(request.data['id'])
    data = {'user': request.user.id, 'recipe': id}
    serializer = serializers.FavoriteSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['DELETE'])
def del_favorite(request, pk):
    recipe = Recipe.objects.get(id=pk)
    Favorite.objects.filter(user=request.user, recipe=recipe).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientsApiView(generics.ListAPIView):
    search_fields = ['title']
    filter_backends = (filters.SearchFilter,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer



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



def formchangerecipe(request):
    return render(
        request,
        'formChangeRecipe.html'
    )


def my_follow(request):
    users = User.objects.filter(following__user=request.user)
    paginator = Paginator(users, 1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)
    return render(
        request,
        'myFollow.html',
        {
            'page_obj': page_obj,
            'paginator': paginator,
        }
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



