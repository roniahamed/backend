from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.core.models import ContactSubmission, Link


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(ModelAdmin):
	list_display = ("id", "name", "email", "service_interest", "status", "created_at")
	list_filter = ("status", "created_at")
	search_fields = ("id", "name", "email", "company", "service_interest", "message")
	readonly_fields = ("created_at",)
	date_hierarchy = "created_at"
	ordering = ("-created_at",)
	list_per_page = 50


@admin.register(Link)
class LinkAdmin(ModelAdmin):
	list_display = ("id", "name", "category", "is_active", "sort_order", "content_type", "object_id")
	list_filter = ("category", "is_active", "content_type")
	search_fields = ("id", "name", "url", "icon")
	ordering = ("category", "sort_order", "name")
	list_select_related = ("content_type",)
	list_per_page = 100
