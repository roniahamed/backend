from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	email = models.EmailField(unique=True)
	full_name = models.CharField(max_length=140)
	title = models.CharField(max_length=120, blank=True)
	bio = models.TextField(blank=True)
	location = models.CharField(max_length=120, blank=True)
	phone = models.CharField(max_length=32, blank=True)
	avatar_url = models.URLField(blank=True)
	github_url = models.URLField(blank=True)
	linkedin_url = models.URLField(blank=True)
	meeting_booking_url = models.URLField(blank=True)
	is_public_profile = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["username"]

	class Meta:
		ordering = ("-date_joined",)

	def __str__(self) -> str:
		return self.full_name or self.email
