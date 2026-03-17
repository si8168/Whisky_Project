from django.db import models
from django.conf import settings
from django.urls import reverse

class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('dessert', 'Dessert'),
    ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(help_text="Short eye-catching intro")
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipe_photos/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    saves = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='saved_recipes', blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_recipes', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # --- Methods ---

    def get_absolute_url(self):
        """Redirects to the recipe detail page after an update/create."""
        return reverse('recipe_detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()
    
    def total_saves(self):
        return self.saves.count()
    
    def __str__(self):
        return self.title

# Unified Review Model (Removed the duplicate below it)
class Review(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star review for {self.recipe.title}"