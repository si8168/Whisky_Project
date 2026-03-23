from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')), 
    
    # --- USER AUTHENTICATION & PROFILE ---
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # PROFILE & EDITING 
    path('profile/', user_views.profile_view, name='profile'), 
    # ADDED: This ensures your 'Modify Credentials' button actually has a destination
    path('profile/edit/', user_views.edit_profile, name='edit_profile'), 

]

# THE VAULT MEDIA & STATIC RECOVERY
if settings.DEBUG:
    # Serves uploaded images (Profile pics, recipe photos)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serves static assets (CSS, JS, Logos)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)