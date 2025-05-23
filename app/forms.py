from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, NewsPost, Tag


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class NewsPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name="default"))
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "tag-select"}),
        required=False,
    )
    new_tags = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter new tags (comma separated)"}
        ),
    )

    class Meta:
        model = NewsPost
        fields = ["title", "summary", "tags", "new_tags", "image", "content"]


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "placeholder": "Write your comment here...",
                "class": "comment-textarea",
            }
        ),
        label="",
    )

    name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your name (optional for guest comments)",
                "class": "comment-name-input",
            }
        ),
    )

    class Meta:
        model = Comment
        fields = ["name", "content"]
