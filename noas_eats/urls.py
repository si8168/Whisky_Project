from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users import views as user_views

# Rename the Admin Panel to Whisky
admin.site.site_header = "Whisky Culinary Administration"
admin.site.site_title = "Whisky Admin Portal"
admin.site.index_title = "Welcome to the Whisky Vault"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    
    # use first
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', user_views.register, name='register'), 
    
    # secondary
    path('accounts/', include('django.contrib.auth.urls')), 
    
    path('profile/', user_views.profile_view, name='profile'),
    path('profile/edit/', user_views.edit_profile_view, name='edit_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)