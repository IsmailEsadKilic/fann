from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    image = models.ImageField(blank=True, upload_to="news_images/")
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
