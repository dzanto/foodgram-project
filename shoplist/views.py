from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from django.views.generic import DetailView, ListView

from rest_framework import filters, status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from . import forms, serializers
from .models import (
    Recipe,
    User,
    Favorite,
    Follow,
    Ingredient,
    Quantity,
    Purchase,
    Tag,
)

from foodgram.settings import PAGINATE_BY

SUCCESS_TRUE = {'success': True}


class RecipeListView(ListView):
    model = Recipe
    template_name = 'index.html'
    paginate_by = PAGINATE_BY

    def get_queryset(self, **kwargs):
        tags = self.request.GET.getlist('tag')
        if tags == []:
            recipes = Recipe.objects.prefetch_related('tags')
            return recipes
        recipes = Recipe.objects.prefetch_related('tags')
        recipes = recipes.filter(tags__title__in=tags).distinct()
        return recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['all_tags'] = Tag.objects.all()
        tags = self.request.GET.getlist('tag')
        if tags == []:
            return context
        context['tags'] = tags
        return context


def authors_recipes(request, author):
    recipe_author = get_object_or_404(User, username=author)
    all_tags = Tag.objects.all()
    tags = request.GET.getlist('tag')
    if tags == []:
        recipes = Recipe.objects.prefetch_related(
            'tags').filter(author=recipe_author)
    else:
        recipes = Recipe.objects.prefetch_related('tags')
        recipes = recipes.filter(tags__title__in=tags, author=recipe_author).distinct()

    page = request.GET.get('page', 1)
    paginator = Paginator(recipes, PAGINATE_BY)
    page_obj = paginator.page(page)

    follow = False
    if request.user.is_authenticated:
        follow = Follow.objects.filter(
            author__username=author).filter(
            user=request.user).exists()

    return render(
        request,
        'index.html',
        {
            'tags': tags,
            'page_obj': page_obj,
            'paginator': paginator,
            'author': recipe_author,
            'follow': follow,
            'all_tags': all_tags,
        }
    )


@login_required
def new_recipe(request):

    labels = {
        'main_title': 'Создание рецепта',
        'button': 'Создать рецепт',
        'del_button': False
    }

    if request.method != 'POST':
        form = forms.RecipeForm()
        return render(
            request,
            'form-recipe.html',
            {'form': form, 'labels': labels}
        )

    form = forms.RecipeForm(request.POST, request.FILES)

    if not form.is_valid():
        return render(request, 'form-recipe.html',
                      {'form': form, 'labels': labels})

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
    return redirect('index')


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
        'main_title': 'Редактирование рецепта',
        'button': 'Сохранить',
        'del_button': True,
        'recipe': recipe
    }

    if request.method != 'POST':
        return render(
            request,
            'form-recipe.html',
            {'form': form, 'ingredients': ingredients, 'labels': labels})

    if not form.is_valid():
        return render(
            request,
            'form-recipe.html',
            {'form': form, 'labels': labels}
        )

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
    return redirect('index')


@login_required
def del_recipe(request, pk):
    get_object_or_404(Recipe, id=pk).delete()
    return redirect('index')


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
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        tags = self.request.GET.getlist('tag')
        recipes = Recipe.objects.filter(favorites__user=self.request.user)
        if tags == []:
            return recipes
        recipes = recipes.filter(tags__title__in=tags).distinct()
        return recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.all()
        tags = self.request.GET.getlist('tag')
        if tags == []:
            return context
        context['tags'] = tags
        return context


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
        p.drawString(100, y, '{} {} {}'.format(key, value[0], value[1]))
        y -= 20
    p.showPage()
    p.save()
    return response


@login_required
def my_follow(request):
    users = User.objects.filter(following__user=request.user)
    paginator = Paginator(users, PAGINATE_BY)
    page = request.GET.get('page', 1)
    page_obj = paginator.page(page)
    return render(
        request,
        'my-follows.html',
        {
            'page_obj': page_obj,
            'paginator': paginator,
        }
    )


def about(request):
    return render(request, 'about.html')


def features(request):
    return render(request, 'features.html')


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


@api_view(['DELETE'])
def del_favorite(request, pk):
    recipe = Recipe.objects.get(id=pk)
    Favorite.objects.filter(user=request.user, recipe=recipe).delete()
    data = SUCCESS_TRUE
    return Response(data, status=status.HTTP_200_OK)


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


@api_view(['DELETE'])
def del_purchase(request, pk):
    recipe = Recipe.objects.get(id=pk)
    Purchase.objects.filter(user=request.user, recipe=recipe).delete()
    data = SUCCESS_TRUE
    return Response(data, status=status.HTTP_200_OK)


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


@api_view(['DELETE'])
def del_follow(request, author):
    author = User.objects.get(username=author)
    Follow.objects.filter(user=request.user, author=author).delete()
    data = SUCCESS_TRUE
    return Response(data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def del_follow_pk(request, pk):
    author = User.objects.get(id=pk)
    Follow.objects.filter(user=request.user, author=author).delete()
    data = SUCCESS_TRUE
    return Response(data, status=status.HTTP_200_OK)


class IngredientsApiView(generics.ListAPIView):
    search_fields = ['title']
    filter_backends = (filters.SearchFilter,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
