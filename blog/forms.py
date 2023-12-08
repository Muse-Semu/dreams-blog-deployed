
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Comment


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']
        # help_texts = {
        #     'username': None,
        #     'email': None,
        #     'password1': None,
        #     'password-confirmation': None
        # }


class UserUpdate(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo','bios','youtube_url','facebook_url','twitter_url','instagram_url','telegram_url']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
