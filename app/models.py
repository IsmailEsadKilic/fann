from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class NewsPost(models.Model):
    title = models.CharField(max_length=200, unique=True, blank=False)
    # many to many relationship with tags
    tags = models.ManyToManyField("Tag", blank=True, related_name="news_posts")
    image = models.ImageField(blank=True, upload_to="news_images/")
    content = RichTextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="news_posts", null=True, blank=True
    )
    published_date = models.DateTimeField(auto_now_add=True)
    summary = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-published_date"]

    def get_absolute_url(self):
        return reverse("news_detail", args=[str(self.id)])


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("tag_detail", args=[str(self.id)])


class Comment(models.Model):
    news_post = models.ForeignKey(
        NewsPost, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments", null=True, blank=True
    )
    name = models.CharField(max_length=100, blank=True)  # For non-authenticated users
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_date"]

    def __str__(self):
        return f"Comment by {self.user.username if self.user else self.name} on {self.news_post.title}"
