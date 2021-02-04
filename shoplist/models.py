from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


def get_user_name(self):
    if self.first_name:
        user_name = '{} {}'.format(self.last_name, self.first_name)
    else:
        user_name = self.username
    return user_name


User.add_to_class("__str__", get_user_name)


class Ingredient(models.Model):
    title = models.CharField(max_length=300, verbose_name='Наименование')
    dimension = models.CharField(max_length=100, verbose_name='Ед.изм')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    title = models.CharField('Имя тега', max_length=50, db_index=True)
    name = models.CharField('Имя тега для шаблона', max_length=50)
    color = models.CharField('Цвет тега', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='recipe/')
    description = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Quantity',
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
    )
    time = models.IntegerField(verbose_name='Время приготовления')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipedetail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Quantity(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='quantities'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='quantities'
    )
    quantity = models.IntegerField(
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )

    class Meta:
        unique_together = ("user", "author")
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites"
    )

    class Meta:
        unique_together = ("user", "recipe")
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="purchases")

    class Meta:
        unique_together = ("user", "recipe")
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
