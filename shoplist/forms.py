from django import forms
from . import models


class RecipeForm(forms.ModelForm):
    class Meta:
        model = models.Recipe
        fields = '__all__'
        exclude = ['author', 'ingredients']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
