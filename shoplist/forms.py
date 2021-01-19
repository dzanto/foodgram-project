from django import forms
from . import models


class RecipeForm(forms.ModelForm):
    class Meta:
        model = models.Recipe
        fields = '__all__'
