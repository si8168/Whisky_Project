from django.urls import path
from . import views

urlpatterns = [
    # --- Landing Page ---
    path('', views.RecipeListView.as_view(), name='home'),
    path('about/', views.about_view, name='about'),
    path('popular/', views.popular_recipes_view, name='popular'),
    path('profile/', views.profile_view, name='profile'),

    # --- Recipe Creation & Management ---
    # FIXED: name='post_recipe' to match your template tags in base.html/home.html
    path('post/', views.RecipeCreateView.as_view(), name='post_recipe'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    
    # NOTE: The name 'recipe_update' is what we must use in search_results.html
    path('recipe/<int:pk>/update/', views.RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipe/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='recipe_delete'),

    # --- Search & Filtering ---
    path('search/', views.search_view, name='search'),
    path('filter/<str:filter_type>/<str:value>/', views.category_view, name='category_view'),

    # --- Interactions ---
    # FIXED: views.like_recipe and views.save_recipe to match the updated views.py
    path('like/<int:pk>/', views.like_recipe, name='like_recipe'),
    path('save/<int:pk>/', views.save_recipe, name='save_recipe'),
]