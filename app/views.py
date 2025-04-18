from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from app import models
from app.forms import CustomUserCreationForm


def index(request):
    news = models.NewsPost.objects.all()
    return render(request, "app/index.html", {"news": news})


def news_detail(request, news_id):
    news = models.NewsPost.objects.get(id=news_id)
    return render(request, "app/news_detail.html", {"news": news})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("index")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})
