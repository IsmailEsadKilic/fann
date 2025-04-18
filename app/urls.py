from django.urls import path

from app import views

urlpatterns = [
    path("", views.index, name="index"),
    path("news/<int:news_id>/", views.news_detail, name="news_detail"),
]
