from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.blog.models import BlogPost, Tag


@admin.register(Tag)
class TagAdmin(ModelAdmin):
	list_display = ("id", "name", "slug")
	search_fields = ("id", "name", "slug")
	prepopulated_fields = {"slug": ("name",)}


@admin.register(BlogPost)
class BlogPostAdmin(ModelAdmin):
	list_display = ("id", "title", "status", "view_count", "published_at", "author")
	list_filter = ("status", "published_at")
	search_fields = ("id", "title", "slug", "excerpt", "content")
	prepopulated_fields = {"slug": ("title",)}
	filter_horizontal = ("tags",)
