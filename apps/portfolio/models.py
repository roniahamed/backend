from django.db import models


class Service(models.Model):
	slug = models.SlugField(unique=True)
	title = models.CharField(max_length=120)
	summary = models.CharField(max_length=240)
	long_description = models.TextField()
	icon_key = models.CharField(max_length=64)
	features = models.JSONField(default=list)
	tech_stack = models.JSONField(default=list)
	sort_order = models.PositiveIntegerField(default=0)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ("sort_order", "title")
		indexes = [
			models.Index(fields=("is_active", "sort_order")),
		]

	def __str__(self) -> str:
		return self.title


class Project(models.Model):
	slug = models.SlugField(unique=True)
	title = models.CharField(max_length=160)
	subtitle = models.CharField(max_length=200, blank=True)
	description = models.TextField()
	abstract = models.TextField(blank=True)
	tech_stack = models.JSONField(default=list)
	user_roles = models.JSONField(default=list)
	security = models.JSONField(default=dict)
	references = models.JSONField(default=dict)
	period = models.CharField(max_length=64, blank=True)
	live_url = models.URLField(blank=True)
	github_url = models.URLField(blank=True)
	category = models.CharField(max_length=60)
	role = models.CharField(max_length=60)
	quote = models.TextField(blank=True)
	problem_statement = models.TextField(blank=True)
	thumbnail_image_url = models.URLField(blank=True)
	is_featured = models.BooleanField(default=False)
	is_published = models.BooleanField(default=True)
	published_at = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ("-published_at", "title")
		indexes = [
			models.Index(fields=("is_published", "published_at")),
			models.Index(fields=("category", "role")),
			models.Index(fields=("slug",)),
		]

	def __str__(self) -> str:
		return self.title


class ProjectImage(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
	image_url = models.URLField()
	title = models.CharField(max_length=120, blank=True)
	sort_order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ("sort_order", "id")
		indexes = [
			models.Index(fields=("project", "sort_order")),
		]


class ProjectMetric(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="metrics")
	label = models.CharField(max_length=120)
	value = models.CharField(max_length=120)
	sort_order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ("sort_order", "id")
		indexes = [
			models.Index(fields=("project", "sort_order")),
		]
