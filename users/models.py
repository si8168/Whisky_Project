from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField # 🌍 The key to the list

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        default='profile_pics/default.png', 
        null=True, 
        blank=True,
        db_column='profile_picture' # 🛠️ Forces the code to look for this specific column
    )
    
    # 🟢 FIXED: Using CountryField inside the class for the dropdown data
    country = CountryField(blank_label='(Select Country)', blank=True)
    
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.username

    @property
    def get_avatar(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return '/static/images/default_archivist.png'

    class Meta:
        # Keeping your premium admin branding exactly as it was
        verbose_name = 'Vault User'
        verbose_name_plural = 'Vault Users'