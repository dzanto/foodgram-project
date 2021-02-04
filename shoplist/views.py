from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic import DetailView
from .models import (
    Recipe,
    User,
    Favorite,
    Follow,
    Ingredient,
    Quantity,
    Purchase
)
from . import forms, serializers
from rest_framework import status
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import filters
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.http import HttpResponse


class RecipeListView(ListView):
    model = Recipe
    template_name = 'index.html'
    paginate_by = 3

    def get_queryset(self, **kwargs):
        tag = self.request.GET.get('tag')
        if tag is None:
            recipes = Recipe.objects.all()
            return recipes
        recipes = Recipe.objects.filter(tags__title__icontains=tag)
        return recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.request.GET.get('tag')
        if tag is None:
            return context
        context['tag'] = tag
        return context


def authors_recipes(request, author):
    recipe_author = get_object_or_404(User, username=author)
    tag = request.GET.get('tag')
    if tag is None:
        recipes = Recipe.objects.filter(author__username=author)
    else:
        recipes = Recipe.objects.filter(
            tags__title__icontains=tag).filter(
            author__username=author
        )

    page = request.GET.get('page', 1)
    paginator = Paginator(recipes, 3)
    page_obj = paginator.page(page)

    follow = False
    if request.user.is_authenticated:
        follow = Follow.objects.filter(
            author__username=author).filter(
            user=request.user).exists()

    return render(
        request,
        "index.html",
        {
            "tag": tag,
            "page_obj": page_obj,
            "paginator": paginator,
            "author": recipe_author,
            "follow": follow,
        }
    )


@login_required
def new_recipe(request):

    labels = {
        "main_title": "Создание рецепта",
        "button": "Создать рецепт",
        "del_button": False
    }

    if request.method != "POST":
        form = forms.RecipeForm()
        return render(
            request,
            "form-recipe.html",
            {"form": form, "labels": labels}
        )

    form = forms.RecipeForm(request.POST, request.FILES)

    if not form.is_valid():
        return render(request, "form-recipe.html",
                      {"form": form, "labels": labels})

    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    form.save_m2m()

    for field in request.POST:
        if 'nameIngredient' in field:
            name_ingredient = request.POST[field]
            value_ingredient = int(request.POST[field.replace('name', 'value')])
            ingredient = Ingredient.objects.get(title=name_ingredient)
            Quantity.objects.get_or_create(
                ingredient=ingredient,
                recipe=recipe,
                quantity=value_ingredient
            )
    return redirect("index")


@login_required
def edit_recipe(request, pk):

    recipe = get_object_or_404(Recipe, id=pk)
    form = forms.RecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    ingredients = Quantity.objects.filter(recipe=recipe)
    labels = {
        "main_title": "Редактирование рецепта",
        "button": "Сохранить",
        "del_button": True,
        "recipe": recipe
    }

    if request.method != "POST":
        return render(
            request,
            "form-recipe.html",
            {"form": form, "ingredients": ingredients, "labels": labels})

    if not form.is_valid():
        return render(
            request,
            "form-recipe.html",
            {"form": form, "labels": labels}
        )

    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    form.save_m2m()

    for field in request.POST:
        print(field)
        if 'nameIngredient' in field:
            name_ingredient = request.POST[field]
            value_ingredient = int(request.POST[field.replace('name', 'value')])
            print(name_ingredient, value_ingredient)
            ingredient = Ingredient.objects.get(title=name_ingredient)
            Quantity.objects.get_or_create(
                ingredient=ingredient,
                recipe=recipe,
                quantity=value_ingredient
            )
    return redirect("index")


@login_required
def del_recipe(request, pk):
    get_object_or_404(Recipe, id=pk).delete()
    return redirect("index")


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'single-recipe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_anonymous:
            return context
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        context['favorite'] = Favorite.objects.filter(
            recipe_id=recipe.id).filter(
            user=self.request.user).exists()
        context['purchase'] = Purchase.objects.filter(
            recipe_id=recipe.id).filter(
            user=self.request.user).exists()
        context['follow'] = Follow.objects.filter(
            author=recipe.author).filter(
            user=self.request.user).exists()
        return context


class FavoriteListView(ListView):
    model = Recipe
    template_name = 'favorite-recipes.html'
    paginate_by = 3

    def get_queryset(self):
        recipes = Recipe.objects.filter(favorites__user=self.request.user)
        return recipes


class PurchaseListView(ListView):
    model = Recipe
    template_name = 'shop-list.html'

    def get_queryset(self):
        recipes = Recipe.objects.filter(purchases__user=self.request.user)
        return recipes


@login_required
def shoplist_generate(request):
    recipes = Recipe.objects.filter(purchases__user=request.user)
    quantities = Quantity.objects.filter(recipe__in=recipes)
    shoplist = {}
    for ing in quantities:
        if shoplist.get(ing.ingredient.title) is None:
            shoplist[ing.ingredient.title] = [
                ing.ingredient.dimension,
                int(ing.quantity)
            ]
        else:
            shoplist[ing.ingredient.title][1] += int(ing.quantity)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="shoplist.pdf"'
    p = canvas.Canvas(response)
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    p.setFont('FreeSans', 16)
    y = 700
    for key, value in shoplist.items():
        p.drawString(100, y, "{} {} {}".format(key, value[0], value[1]))
        y -= 20
    p.showPage()
    p.save()
    return response


@login_required
def my_follow(request):
    users = User.objects.filter(following__user=request.user)
    paginator = Paginator(users, 1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)
    return render(
        request,
        'my-follows.html',
        {
            'page_obj': page_obj,
            'paginator': paginator,
        }
    )


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
    data = {"success": True}
    return Response(data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def add_purchase(request):
    id = int(request.data['id'])
    data = {'user': request.user.id, 'recipe': id}
    serializer = serializers.PurchaseSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['DELETE'])
def del_purchase(request, pk):
    recipe = Recipe.objects.get(id=pk)
    Purchase.objects.filter(user=request.user, recipe=recipe).delete()
    data = {"success": True}
    return Response(data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def add_follow(request):
    author_name = request.data['id']
    author = User.objects.get(username=author_name)
    data = {'user': request.user.id, 'author': author.id}
    serializer = serializers.FollowSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    return Response(data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['DELETE'])
def del_follow(request, author):
    author = User.objects.get(username=author)
    Follow.objects.filter(user=request.user, author=author).delete()
    data = {"success": True}
    return Response(data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['DELETE'])
def del_follow_pk(request, pk):
    print(pk)
    author = User.objects.get(id=pk)
    print(author)
    Follow.objects.filter(user=request.user, author=author).delete()
    data = {"success": True}
    return Response(data, status=status.HTTP_200_OK)


class IngredientsApiView(generics.ListAPIView):
    search_fields = ['title']
    filter_backends = (filters.SearchFilter,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
