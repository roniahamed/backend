from django.contrib import admin

from apps.core.models import ContactSubmission


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "service_interest", "status", "created_at")
	list_filter = ("status", "created_at")
	search_fields = ("name", "email", "company", "service_interest")
