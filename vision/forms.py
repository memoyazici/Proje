from django import forms

from .models import Post
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('author','title', 'text', 'image',)
        
class CustomUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password')