from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from app import models
from app.forms import CustomUserCreationForm, NewsPostForm


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


@login_required
def publish_news_post(request):
    if request.method == "POST":
        form = NewsPostForm(request.POST, request.FILES)
        if form.is_valid():
            news_post = form.save(commit=False)
            news_post.user = request.user
            news_post.save()
            return redirect("news_detail", news_id=news_post.id)
    else:
        form = NewsPostForm()
    return render(request, "app/publish_news_post.html", {"form": form})

@login_required

def edit_news_post(request, news_id):
    post = get_object_or_404(models.NewsPost, id=news_id)

    if request.method == "POST":
        form = NewsPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('news_detail', news_id=post.id)  
    else:
        form = NewsPostForm(instance=post)

    return render(request, 'app/publish_news_post.html', {'form': form, 'post': post, 'edit': True})
