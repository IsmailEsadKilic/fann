from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from app import models
from app.forms import CommentForm, CustomUserCreationForm, NewsPostForm


def index(request):
    news = models.NewsPost.objects.all()
    return render(request, "app/index.html", {"news": news})


def news_detail(request, news_id):
    news = get_object_or_404(models.NewsPost, id=news_id)
    comments = news.comments.all()

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.news_post = news
            if request.user.is_authenticated:
                comment.user = request.user
            comment.save()
            return redirect("news_detail", news_id=news_id)
    else:
        comment_form = CommentForm()

    return render(
        request,
        "app/news_detail.html",
        {"news": news, "comments": comments, "comment_form": comment_form},
    )


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

            # Handle existing tags
            form.save_m2m()  # Save many-to-many relationships

            # Handle new tags
            new_tags = form.cleaned_data.get("new_tags", "").strip()
            if new_tags:
                tag_names = [t.strip() for t in new_tags.split(",") if t.strip()]
                for tag_name in tag_names:
                    tag, created = models.Tag.objects.get_or_create(name=tag_name)
                    news_post.tags.add(tag)

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
            news_post = form.save()

            # Handle new tags
            new_tags = form.cleaned_data.get("new_tags", "").strip()
            if new_tags:
                tag_names = [t.strip() for t in new_tags.split(",") if t.strip()]
                for tag_name in tag_names:
                    tag, created = models.Tag.objects.get_or_create(name=tag_name)
                    news_post.tags.add(tag)

            return redirect("news_detail", news_id=post.id)
    else:
        form = NewsPostForm(instance=post)

    return render(
        request,
        "app/publish_news_post.html",
        {"form": form, "post": post, "edit": True},
    )


@login_required
def delete_news_post(request, news_id):
    post = get_object_or_404(models.NewsPost, id=news_id)
    if request.user == post.user:
        post.delete()
        return redirect("index")
    else:
        return redirect("news_detail", news_id=news_id)
