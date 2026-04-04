from rest_framework import serializers

from apps.core.models import ContactSubmission


class ContactSubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = (
            "name",
            "email",
            "company",
            "service_interest",
            "message",
        )

    def validate_message(self, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned) < 20:
            raise serializers.ValidationError("Message must be at least 20 characters.")
        return cleaned
