from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from recipes.models import Recipe
from .forms import UserUpdateForm 

@login_required
def profile_view(request):
    # This must be named 'user_recipes' to match your profile.html loop
    user_recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    liked_recipes = request.user.liked_recipes.all().order_by('-created_at')
    # This must be named 'saved_recipes' for your "Saved for Later" section
    saved_recipes = request.user.saved_recipes.all().order_by('-created_at')
    
    return render(request, 'users/profile.html', {
        'user_recipes': user_recipes,  # Key must match the template variable
        'liked_recipes': liked_recipes,
        'saved_recipes': saved_recipes,
    })

@login_required
def saved_recipes_page(request):
    # Only show saved recipes here
    saved_recipes = request.user.saved_recipes.all().order_by('-created_at')
    return render(request, 'recipes/saved.html', {'saved_recipes': saved_recipes})

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        # request.FILES is crucial for uploading images!
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})