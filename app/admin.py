from django.contrib import admin

from .models import NewsPost


class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_date")
    search_fields = ("title", "category")
    list_filter = ("category", "published_date")
    ordering = ("-published_date",)
    date_hierarchy = "published_date"


admin.site.register(NewsPost, NewsAdmin)
