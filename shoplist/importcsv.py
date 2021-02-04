import csv
from shoplist.models import Ingredient, Tag
with open('ingredients.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        _, created = Ingredient.objects.get_or_create(
            title=row[0],
            dimension=row[1],
        )
Tag.objects.get_or_create(title='breakfast', name='Завтрак', color='green')
Tag.objects.get_or_create(title='lunch', name='Обед', color='orange')
Tag.objects.get_or_create(title='dinner', name='Ужин', color='purple')
