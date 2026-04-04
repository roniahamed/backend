import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from apps.core.models import ContactSubmission, Link
from apps.core.serializers import ContactSubmissionCreateSerializer, LinkSerializer

logger = logging.getLogger(__name__)


class ContactSubmissionThrottle(AnonRateThrottle):
	scope = "contact_submission"


class HealthCheckView(APIView):
	permission_classes = [AllowAny]

	def get(self, request):
		return Response({"status": "ok", "timestamp": timezone.now()})


class ContactSubmissionCreateView(generics.CreateAPIView):
	permission_classes = [AllowAny]
	serializer_class = ContactSubmissionCreateSerializer
	queryset = ContactSubmission.objects.all()
	throttle_classes = [ContactSubmissionThrottle]

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		try:
			with transaction.atomic():
				submission = serializer.save()
				# why: Immediate SMTP send confirms lead intake without background queue.
				recipient = settings.CONTACT_RECEIVER_EMAIL
				sent = send_mail(
					subject=f"[Portfolio Contact] {submission.service_interest or 'General Inquiry'}",
					message=(
						f"Name: {submission.name}\n"
						f"Email: {submission.email}\n"
						f"Company: {submission.company or 'N/A'}\n"
						f"Service Interest: {submission.service_interest or 'N/A'}\n\n"
						f"Message:\n{submission.message}"
					),
					from_email=settings.DEFAULT_FROM_EMAIL,
					recipient_list=[recipient],
					fail_silently=False,
				)
				if sent == 0:
					raise APIException("Email delivery failed. Please try again.")
		except Exception as exc:
			logger.exception("Failed to process contact submission")
			raise APIException("Unable to submit contact form at this time.") from exc

		return Response(serializer.data, status=201)


class LinkViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [AllowAny]
	serializer_class = LinkSerializer
	queryset = Link.objects.filter(is_active=True).select_related("content_type")
	filterset_fields = ("category", "is_active", "content_type")
	search_fields = ("name", "url", "icon")
	ordering_fields = ("sort_order", "name", "id")
