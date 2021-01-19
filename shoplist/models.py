from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from multiselectfield import MultiSelectField

User = get_user_model()


def get_user_name(self):
    if self.first_name:
        user_name = '{} {}'.format(self.last_name, self.first_name)
    else:
        user_name = self.username
    return user_name


User.add_to_class("__str__", get_user_name)


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


class Tag(models.Model):
    mealtime = models.CharField(max_length=7)

    def __str__(self):
        return self.mealtime


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='recipe/')
    description = models.TextField(default='Описание')
    ingredients = models.ManyToManyField(Ingredient, through='Quantity', null=True, blank=True)
    # tag = models.CharField(
    #     max_length=10,
    #     choices=TAGS,
    #     verbose_name='Tag',
    # )
    # tag = models.ManyToManyField(Tag)
    tag = MultiSelectField(choices=TAGS, default=[1])
    time = models.IntegerField(verbose_name='Время приготовления')
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('singlepagenotauth', args=[str(self.slug)])


class Quantity(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,)
    quantity = models.IntegerField(verbose_name='Количество')
