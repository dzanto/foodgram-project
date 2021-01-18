import csv
from shoplist.models import Ingredient
with open('ingredients.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        _, created = Ingredient.objects.get_or_create(
            title=row[0],
            dimension=row[1],
        )
