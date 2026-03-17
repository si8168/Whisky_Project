from django.urls import path
from . import views

urlpatterns = [
    # --- Landing Page ---
    path('', views.RecipeListView.as_view(), name='home'),
    path('about/', views.about_view, name='about'),
    path('popular/', views.popular_recipes_view, name='popular'),

    # --- Recipe Creation & Management ---
    # We are using RecipeCreateView (Class) instead of post_recipe_view (Function)
    path('post/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/<int:pk>/update/', views.RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipe/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='recipe_delete'),

    # --- Search & Filtering ---
    path('search/', views.search_view, name='search'),
    path('category/<str:category_name>/', views.category_view, name='category_view'),

    # --- Interactions ---
    path('like/<int:pk>/', views.like_recipe_view, name='like_recipe'),
    path('save/<int:pk>/', views.save_recipe_view, name='save_recipe'),
]