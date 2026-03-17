from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Recipe
from .forms import RecipeForm

# --- LIST VIEWS (Home, Popular, Category, Search) ---

class RecipeListView(ListView):
    """Phase 1: Displays the main recipe feed on the landing page."""
    model = Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Noa's Eats"
        return context

def popular_recipes_view(request):
    """Shows top 10 recipes based on likes."""
    popular_recipes = Recipe.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:10]
    return render(request, 'recipes/home.html', {'recipes': popular_recipes, 'title': 'Popular Eats'})

def category_view(request, category_name):
    """Phase 1: Filters recipes by category (Breakfast, Lunch, Dinner, etc.)."""
    recipes = Recipe.objects.filter(category__iexact=category_name).order_by('-created_at')
    return render(request, 'recipes/home.html', {
        'recipes': recipes, 
        'title': category_name.replace('-', ' ').title()
    })

def search_view(request):
    """Phase 2: Search bar functionality for keywords in title/ingredients."""
    query = request.GET.get('q', '')
    results = Recipe.objects.filter(
        Q(title__icontains=query) | 
        Q(description__icontains=query) | 
        Q(ingredients__icontains=query)
    ).distinct() if query else []
    return render(request, 'recipes/search_results.html', {'results': results, 'query': query})

# --- DETAIL & CRUD VIEWS ---

class RecipeDetailView(DetailView):
    """Phase 1: Detailed view of a single recipe."""
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

class RecipeCreateView(LoginRequiredMixin, CreateView):
    """Phase 2: Allows logged-in users to submit new recipes."""
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/post_recipe.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Phase 2: Allows authors to edit their own recipes."""
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/post_recipe.html'
    
    def test_func(self):
        return self.request.user == self.get_object().author

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Phase 2: Allows authors to delete their own recipes."""
    model = Recipe
    success_url = '/'
    template_name = 'recipes/recipe_confirm_delete.html'
    
    def test_func(self):
        return self.request.user == self.get_object().author

# --- INTERACTION & STATIC VIEWS ---

@login_required
def like_recipe_view(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.likes.filter(id=request.user.id).exists():
        recipe.likes.remove(request.user)
    else:
        recipe.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def save_recipe_view(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.saves.filter(id=request.user.id).exists():
        recipe.saves.remove(request.user)
    else:
        recipe.saves.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def about_view(request):
    return render(request, 'recipes/about.html', {'title': 'About Noa\'s Eats'})