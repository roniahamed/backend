from django.conf import settings
from django.db import models
from django.utils import timezone


class Tag(models.Model):
	name = models.CharField(max_length=60, unique=True)
	slug = models.SlugField(unique=True)

	class Meta:
		ordering = ("name",)

	def __str__(self) -> str:
		return self.name


class BlogPost(models.Model):
	STATUS_DRAFT = "draft"
	STATUS_PUBLISHED = "published"

	STATUS_CHOICES = (
		(STATUS_DRAFT, "Draft"),
		(STATUS_PUBLISHED, "Published"),
	)

	slug = models.SlugField(unique=True)
	title = models.CharField(max_length=160)
	excerpt = models.CharField(max_length=280)
	content = models.TextField()
	cover_image_url = models.URLField(blank=True)
	status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_DRAFT)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="blog_posts")
	tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
	reading_time_minutes = models.PositiveIntegerField(default=1)
	view_count = models.IntegerField(default=0)
	meta_description = models.CharField(max_length=180, blank=True)
	published_at = models.DateTimeField(default=timezone.now)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ("-published_at",)
		indexes = [
			models.Index(fields=("status", "published_at")),
			models.Index(fields=("slug",)),
		]

	def __str__(self) -> str:
		return self.title
