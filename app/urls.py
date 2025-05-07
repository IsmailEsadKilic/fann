from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import RedirectView

from app import views

urlpatterns = [
    path("", views.index, name="index"),
    path("news/<int:news_id>/", views.news_detail, name="news_detail"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path(
        "accounts/logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"
    ),
    path("accounts/register/", views.register, name="register"),
    path(
        "accounts/profile/",
        RedirectView.as_view(url="/", permanent=False),
        name="profile",
    ),
    path(
        "profile/", RedirectView.as_view(url="/", permanent=False), name="profile_alt"
    ),
    path(   
        "user/<str:username>/",
        RedirectView.as_view(url="/", permanent=False),
        name="user_profile",
    ),

    path("publish/", views.publish_news_post, name="publish_news_post"),
    path("edit_news_post/<int:news_id>/", views.edit_news_post, name="edit_news_post"),
    path("delete_post/<int:news_id>/", views.delete_news_post, name="delete_news_post"),
]
