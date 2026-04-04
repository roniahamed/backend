from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.users.models import User


@admin.register(User)
class UserAdmin(ModelAdmin):
	list_display = ("id", "email", "full_name", "is_public_profile", "is_staff")
	list_filter = ("is_public_profile", "is_staff", "is_active")
	search_fields = ("id", "email", "full_name", "username")
