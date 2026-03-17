from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'category', 'image', 'ingredients', 'instructions']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'A catchy intro...'}),
            'ingredients': forms.Textarea(attrs={'rows': 5}),
            'instructions': forms.Textarea(attrs={'rows': 5}),
        }