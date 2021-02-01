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
    title = models.CharField('Имя тега', max_length=20, db_index=True)
    name = models.CharField('Имя тега для шаблона', max_length=20)
    color = models.CharField('Цвет тега', max_length=20)

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
    description = models.TextField(default='Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Quantity',
        blank=True,
    )
    # tag = models.CharField(
    #     max_length=10,
    #     choices=TAGS,
    #     verbose_name='Tag',
    # )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
    )
    # tag = MultiSelectField(choices=TAGS)
    time = models.IntegerField(verbose_name='Время приготовления')
    # slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipedetail', args=[str(self.id)])


class Quantity(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='quantities')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,)
    quantity = models.IntegerField(verbose_name='Количество')


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    class Meta:
        unique_together = ("user", "author")


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="favorites")

    class Meta:
        unique_together = ("user", "recipe")


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="purchases")

    class Meta:
        unique_together = ("user", "recipe")
