from django.contrib import admin

from apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ("email", "full_name", "is_public_profile", "is_staff")
	search_fields = ("email", "full_name")
