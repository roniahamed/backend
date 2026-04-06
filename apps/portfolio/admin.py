from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from apps.portfolio.models import Project, ProjectImage, ProjectMetric, Service


class ProjectImageInline(TabularInline):
	model = ProjectImage
	extra = 1
	ordering = ("sort_order", "id")


class ProjectMetricInline(TabularInline):
	model = ProjectMetric
	extra = 1
	ordering = ("sort_order", "id")


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
	list_display = ("id", "title", "slug", "is_active", "sort_order")
	list_filter = ("is_active",)
	search_fields = ("title", "slug")
	prepopulated_fields = {"slug": ("title",)}
	ordering = ("sort_order", "title")
	list_per_page = 50


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
	list_display = ("id", "title", "slug", "category", "role", "is_open_source", "is_featured", "is_published")
	list_filter = ("is_open_source", "is_featured", "is_published", "category", "role")
	search_fields = ("title", "slug", "category", "role")
	prepopulated_fields = {"slug": ("title",)}
	inlines = (ProjectImageInline, ProjectMetricInline)
	date_hierarchy = "published_at"
	ordering = ("-published_at", "title")
	list_per_page = 30
	fieldsets = (
		("Basic Information", {
			"fields": ("title", "slug", "subtitle", "description", "abstract", "thumbnail_image_url")
		}),
		("Classification & Status", {
			"fields": ("category", "role", "is_open_source", "is_featured", "is_published", "published_at")
		}),
		("External Links", {
			"fields": ("live_url", "github_url")
		}),
		("Case Study Data (JSON Arrays/Dicts)", {
			"fields": (
				"tech_stack", "user_roles", "security", "references", "period", 
				"quote", "problem_statement", "challenges", "solutions", 
				"feature_items", "technical_architecture", "impact_metrics"
			),
			"description": "Enter data as raw JSON (e.g. [\"React\", \"Django\"] for arrays, or {\"key\": \"value\"} for objects). Check the frontend models for exact schema requirements."
		})
	)
