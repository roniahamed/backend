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
