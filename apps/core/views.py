from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from apps.core.models import ContactSubmission
from apps.core.serializers import ContactSubmissionCreateSerializer


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
