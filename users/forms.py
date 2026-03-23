from django import forms
from .models import CustomUser
from django_countries.widgets import CountrySelectWidget # Crucial for the dropdown

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # Matches your CustomUser model fields exactly
        fields = ['username', 'email', 'profile_picture', 'country', 'bio']
        
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            # Updated with form-control class to match the new dark CSS
            'country': CountrySelectWidget(attrs={
                'class': 'form-control', 
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Tell the vault about your culinary journey...'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        # Keeping your custom labels for that premium feel
        self.fields['profile_picture'].label = "Profile Portrait"
        self.fields['country'].label = "Origin / Country"