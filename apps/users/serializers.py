from rest_framework import serializers

from apps.users.models import User


class PublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "title",
            "bio",
            "location",
            "email",
            "phone",
            "github_url",
            "linkedin_url",
            "meeting_booking_url",
            "avatar_url",
        )
