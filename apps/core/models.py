from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ContactSubmission(models.Model):
	STATUS_NEW = "new"
	STATUS_REVIEWED = "reviewed"
	STATUS_REPLIED = "replied"

	STATUS_CHOICES = (
		(STATUS_NEW, "New"),
		(STATUS_REVIEWED, "Reviewed"),
		(STATUS_REPLIED, "Replied"),
	)

	name = models.CharField(max_length=120)
	email = models.EmailField()
	company = models.CharField(max_length=120, blank=True)
	service_interest = models.CharField(max_length=120, blank=True)
	message = models.TextField()
	status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_NEW)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ("-created_at",)
		indexes = [
			models.Index(fields=("status", "created_at")),
		]

	def __str__(self) -> str:
		return f"{self.name} <{self.email}>"


class Link(models.Model):
	CATEGORY_DEVELOPER = "developer"
	CATEGORY_PROFESSIONAL = "professional"
	CATEGORY_SOCIAL = "social"
	CATEGORY_REFERENCE = "reference"

	CATEGORY_CHOICES = (
		(CATEGORY_DEVELOPER, "Developer"),
		(CATEGORY_PROFESSIONAL, "Professional"),
		(CATEGORY_SOCIAL, "Social"),
		(CATEGORY_REFERENCE, "Reference"),
	)

	name = models.CharField(max_length=120)
	url = models.URLField(max_length=500)
	icon = models.CharField(max_length=60, blank=True)
	category = models.CharField(max_length=24, choices=CATEGORY_CHOICES, default=CATEGORY_REFERENCE)
	sort_order = models.PositiveIntegerField(default=0)
	is_active = models.BooleanField(default=True)

	# why: Generic relation keeps one link table reusable across domain models.
	content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
	object_id = models.PositiveBigIntegerField(null=True, blank=True)
	content_object = GenericForeignKey("content_type", "object_id")

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ("sort_order", "name")
		indexes = [
			models.Index(fields=("category", "is_active", "sort_order")),
			models.Index(fields=("content_type", "object_id")),
		]

	def __str__(self) -> str:
		return self.name
