import logging

from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from apps.core.models import ContactSubmission
from apps.core.serializers import (
	ContactSubmissionCreateSerializer,
	LinkSerializer,
	ProjectCoverUploadSerializer,
)
from apps.core.services.contact_service import create_submission_and_enqueue_email
from apps.core.services.health_service import get_health_payload
from apps.core.services.link_service import get_active_links_queryset
from apps.portfolio.services.media_service import upload_project_cover_and_enqueue

logger = logging.getLogger(__name__)


class ContactSubmissionThrottle(AnonRateThrottle):
	scope = "contact_submission"


class HealthCheckView(APIView):
	permission_classes = [AllowAny]

	def get(self, request):
		payload, status_code = get_health_payload()
		return Response(payload, status=status_code)


class ContactSubmissionCreateView(generics.CreateAPIView):
	permission_classes = [AllowAny]
	serializer_class = ContactSubmissionCreateSerializer
	queryset = ContactSubmission.objects.all()
	throttle_classes = [ContactSubmissionThrottle]

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		try:
			submission = create_submission_and_enqueue_email(validated_payload=serializer.validated_data)
		except Exception:
			logger.exception("Failed to create contact submission")
			raise

		response_serializer = self.get_serializer(submission)
		return Response(response_serializer.data, status=201)


class LinkViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [AllowAny]
	serializer_class = LinkSerializer
	queryset = get_active_links_queryset()
	filterset_fields = ("category", "is_active", "content_type")
	search_fields = ("name", "url", "icon")
	ordering_fields = ("sort_order", "name", "id")


class ProjectCoverUploadView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		serializer = ProjectCoverUploadSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		result = upload_project_cover_and_enqueue(
			project_slug=serializer.validated_data["project_slug"],
			image_file=serializer.validated_data["file"],
		)
		return Response(result, status=202)
