from django.contrib import admin

from .models import NewsPost, Tag


class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "get_tags", "published_date")
    search_fields = ("title",)
    list_filter = ("published_date", "tags")
    ordering = ("-published_date",)
    date_hierarchy = "published_date"

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = "Tags"


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")


admin.site.register(NewsPost, NewsAdmin)
admin.site.register(Tag, TagAdmin)
