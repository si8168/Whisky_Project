from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):  # You need this class line!
    class Meta:
        model = Recipe
        fields = [
            'title', 
            'meal_type', 
            'diet_requirement', 
            'event_tag', 
            'description', 
            'ingredients', 
            'instructions', 
            'image'
        ]
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'A short, eye-catching intro...'}),
            'ingredients': forms.Textarea(attrs={'rows': 5}),
            'instructions': forms.Textarea(attrs={'rows': 5}),
        }