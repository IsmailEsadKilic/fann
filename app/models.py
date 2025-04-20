from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


class NewsPost(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    image = models.ImageField(blank=True, upload_to="news_images/")
    content = RichTextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_posts', null=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
