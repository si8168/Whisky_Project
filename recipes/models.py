from django.db import models
from django.conf import settings
from django.urls import reverse

class Recipe(models.Model):
    # --- Category Choice Tiers ---
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast'), ('lunch', 'Lunch'), 
        ('dinner', 'Dinner'), ('dessert', 'Dessert'), ('drinks', 'Drinks'),
    ]
    DIET_CHOICES = [
        ('none', 'No Dietary Preference'), ('keto', 'Keto'), 
        ('vegetarian', 'Vegetarian'), ('vegan', 'Vegan'), ('gluten-free', 'Gluten-Free'),
    ]
    EVENT_CHOICES = [
        ('none', 'Standard Recipe'), 
        ('birthday', 'Birthday'), 
        ('mothers-day', "Mother's Day"), 
        ('valentines-day', "Valentine's Day"),
        ('christmas', 'Christmas'), 
        ('halloween', 'Halloween'),
        ('st-patricks', "St. Patrick's Day"), 
        ('easter', 'Easter'),                 
        ('eid', 'Eid'),                       
        ('anniversary', 'Anniversary'),       
        ('wedding', 'Wedding'),               
    ]

    # --- Basic Info ---
    title = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(help_text="Short eye-catching intro")
    ingredients = models.TextField()
    instructions = models.TextField()
    
    # Updated: blank=True/null=True allows you to post recipes without an image if needed
    image = models.ImageField(upload_to='recipe_photos/', blank=True, null=True)

    # --- The Three Tiers (Replacing the old category field) ---
    meal_type = models.CharField(max_length=50, choices=MEAL_CHOICES, default='dinner')
    diet_requirement = models.CharField(max_length=50, choices=DIET_CHOICES, default='none')
    event_tag = models.CharField(max_length=50, choices=EVENT_CHOICES, default='none')
    
    # --- Interactions & Metadata ---
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

class Review(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star review for {self.recipe.title}"