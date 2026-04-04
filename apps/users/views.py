from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import User
from apps.users.serializers import PublicProfileSerializer


class PublicProfileView(APIView):
	permission_classes = [AllowAny]

	def get(self, request):
		# why: Portfolio has one public profile; latest avoids hardcoded IDs.
		profile = User.objects.filter(is_public_profile=True).order_by("-updated_at").first()
		if profile is None:
			return Response({"detail": "Profile not configured yet."}, status=404)
		serializer = PublicProfileSerializer(profile)
		return Response(serializer.data)
