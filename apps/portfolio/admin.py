from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from apps.portfolio.models import Project, ProjectImage, ProjectMetric, Service


class ProjectImageInline(TabularInline):
	model = ProjectImage
	extra = 1


class ProjectMetricInline(TabularInline):
	model = ProjectMetric
	extra = 1


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
	list_display = ("id", "title", "slug", "is_active", "sort_order")
	list_filter = ("is_active",)
	search_fields = ("id", "title", "slug", "summary", "long_description")
	prepopulated_fields = {"slug": ("title",)}


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
	list_display = ("id", "title", "slug", "category", "role", "is_open_source", "is_featured", "is_published")
	list_filter = ("is_open_source", "is_featured", "is_published", "category", "role")
	search_fields = ("id", "title", "slug", "description", "abstract")
	prepopulated_fields = {"slug": ("title",)}
	inlines = (ProjectImageInline, ProjectMetricInline)
