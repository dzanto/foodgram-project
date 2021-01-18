from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование')
    dimension = models.CharField(max_length=5, verbose_name='Ед.изм.')

    def __str__(self):
        return self.title


TAGS = (
    ('breakfast', 'Завтрак'),
    ('lunch', 'Обед'),
    ('dinner', 'Ужин'),
)


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='recipe/')
    description = models.TextField
    ingredients = models.ManyToManyField(Ingredient, through='Quantity')
    tag = models.CharField(
        max_length=10,
        choices=TAGS,
        verbose_name='Tag',
    )
    time = models.IntegerField(verbose_name='Время приготовления')
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Quantity(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,)
    quantity = models.IntegerField(verbose_name='Количество')
