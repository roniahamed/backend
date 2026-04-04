from django.contrib import admin

from apps.portfolio.models import Project, ProjectImage, ProjectMetric, Service


class ProjectImageInline(admin.TabularInline):
	model = ProjectImage
	extra = 1


class ProjectMetricInline(admin.TabularInline):
	model = ProjectMetric
	extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
	list_display = ("title", "slug", "is_active", "sort_order")
	list_filter = ("is_active",)
	search_fields = ("title", "summary")
	prepopulated_fields = {"slug": ("title",)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = ("title", "slug", "category", "role", "is_featured", "is_published")
	list_filter = ("is_featured", "is_published", "category", "role")
	search_fields = ("title", "description", "abstract")
	prepopulated_fields = {"slug": ("title",)}
	inlines = (ProjectImageInline, ProjectMetricInline)
