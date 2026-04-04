from django.contrib import admin

from apps.blog.models import BlogPost, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ("name", "slug")
	search_fields = ("name",)
	prepopulated_fields = {"slug": ("name",)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
	list_display = ("title", "status", "published_at", "author")
	list_filter = ("status", "published_at")
	search_fields = ("title", "excerpt", "content")
	prepopulated_fields = {"slug": ("title",)}
	filter_horizontal = ("tags",)
