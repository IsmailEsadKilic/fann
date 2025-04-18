from django.shortcuts import render

from app import models


def index(request):
    news = models.NewsPost.objects.all()
    return render(request, "app/index.html", {"news": news})


def news_detail(request, news_id):
    news = models.NewsPost.objects.get(id=news_id)
    return render(request, "app/news_detail.html", {"news": news})
