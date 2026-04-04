from rest_framework import serializers

from apps.core.models import ContactSubmission, Link


class LinkSerializer(serializers.ModelSerializer):
    related_object_type = serializers.SerializerMethodField()
    related_object_id = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = (
            "id",
            "name",
            "url",
            "icon",
            "category",
            "sort_order",
            "is_active",
            "related_object_type",
            "related_object_id",
        )

    def get_related_object_type(self, obj: Link) -> str | None:
        return obj.content_type.model if obj.content_type_id else None

    def get_related_object_id(self, obj: Link) -> int | None:
        return obj.object_id


class ContactSubmissionCreateSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = ContactSubmission
        fields = (
            "name",
            "email",
            "company",
            "subject",
            "service_interest",
            "message",
        )

    def validate_message(self, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned) < 20:
            raise serializers.ValidationError("Message must be at least 20 characters.")
        return cleaned

    def validate(self, attrs):
        if not attrs.get("service_interest") and attrs.get("subject"):
            attrs["service_interest"] = attrs["subject"]
        return attrs

    def create(self, validated_data):
        validated_data.pop("subject", None)
        return super().create(validated_data)
