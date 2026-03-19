from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm # Added for registration
from recipes.models import Recipe
from .forms import UserUpdateForm 

# --- NEW: REGISTRATION VIEW ---
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# --- PROFILE VIEW ---
@login_required
def profile_view(request):
    user_recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    liked_recipes = request.user.liked_recipes.all().order_by('-created_at')
    saved_recipes = request.user.saved_recipes.all().order_by('-created_at')
    
    return render(request, 'users/profile.html', {
        'user_recipes': user_recipes,
        'liked_recipes': liked_recipes,
        'saved_recipes': saved_recipes,
    })

# --- SAVED RECIPES PAGE ---
@login_required
def saved_recipes_page(request):
    saved_recipes = request.user.saved_recipes.all().order_by('-created_at')
    return render(request, 'recipes/saved.html', {'saved_recipes': saved_recipes})

# --- EDIT PROFILE ---
@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})