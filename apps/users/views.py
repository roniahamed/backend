from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import PublicProfileSerializer
from apps.users.services.profile_service import get_latest_public_profile


class PublicProfileView(APIView):
	permission_classes = [AllowAny]

	def get(self, request):
		profile = get_latest_public_profile()
		if profile is None:
			return Response({"detail": "Profile not configured yet."}, status=404)
		serializer = PublicProfileSerializer(profile)
		return Response(serializer.data)
