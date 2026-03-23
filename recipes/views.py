from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Recipe
from .forms import RecipeForm

# --- LIST VIEWS (Home, Popular, Category, Search) ---

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Whisky" 
        return context

def popular_recipes_view(request):
    popular_recipes = Recipe.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:10]
    return render(request, 'recipes/home.html', {'recipes': popular_recipes, 'title': 'Popular Eats'})

def category_view(request, filter_type, value): 
    filter_kwargs = {f"{filter_type}__iexact": value}
    recipes = Recipe.objects.filter(**filter_kwargs).order_by('-created_at')
    
    return render(request, 'recipes/home.html', {
        'recipes': recipes,
        'title': value.replace('-', ' ').title()
    })

def search_view(request):
    query = request.GET.get('q')
    if query:
        results = Recipe.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(meal_type__icontains=query) |
            Q(diet_requirement__icontains=query) |
            Q(event_tag__icontains=query)
        ).distinct()
    else:
        results = Recipe.objects.none()
        
    return render(request, 'recipes/search_results.html', {'results': results, 'query': query})

# --- DETAIL & CRUD VIEWS ---

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/post_recipe.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/post_recipe.html'
    
    def test_func(self):
        return self.request.user == self.get_object().author

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = '/'
    template_name = 'recipes/recipe_confirm_delete.html'
    
    def test_func(self):
        return self.request.user == self.get_object().author

# --- INTERACTION & STATIC VIEWS ---

@login_required
def like_recipe(request, pk):  # FIXED: Renamed to match template tags
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.likes.filter(id=request.user.id).exists():
        recipe.likes.remove(request.user)
    else:
        recipe.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def save_recipe(request, pk):  # FIXED: Renamed to match template tags
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.saves.filter(id=request.user.id).exists():
        recipe.saves.remove(request.user)
    else:
        recipe.saves.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def profile_view(request):
    liked_recipes = request.user.liked_recipes.all()
    saved_recipes = request.user.saved_recipes.all()
    # FIXED: context variable renamed to 'user_recipes' to match profile.html
    user_recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    
    return render(request, 'users/profile.html', {
        'liked_recipes': liked_recipes,
        'saved_recipes': saved_recipes,
        'user_recipes': user_recipes,
        'title': f"{request.user.username}'s Profile"
    })

def about_view(request):
    return render(request, 'recipes/about.html', {'title': 'About Whisky'})