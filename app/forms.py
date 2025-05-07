from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget
from .models import NewsPost


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]  # Remove email field


class NewsPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='default'))
    
    class Meta:
        model = NewsPost
        fields = ['title', 'image', 'content']
