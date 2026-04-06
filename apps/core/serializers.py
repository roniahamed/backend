from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.html import strip_tags
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
        if not obj.content_type_id:
            return None
        return ContentType.objects.get_for_id(obj.content_type_id).model

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
        cleaned = strip_tags(value).strip()
        if len(cleaned) < 20:
            raise serializers.ValidationError("Message must be at least 20 characters.")
        return cleaned

    def validate_name(self, value: str) -> str:
        cleaned = strip_tags(value).strip()
        if not cleaned:
            raise serializers.ValidationError("Name is required.")
        return cleaned

    def validate_company(self, value: str) -> str:
        return strip_tags(value).strip()

    def validate_service_interest(self, value: str) -> str:
        return strip_tags(value).strip()

    def validate(self, attrs):
        if not attrs.get("service_interest") and attrs.get("subject"):
            attrs["service_interest"] = attrs["subject"]
        return attrs

    def create(self, validated_data):
        validated_data.pop("subject", None)
        return super().create(validated_data)


class ProjectCoverUploadSerializer(serializers.Serializer):
    project_slug = serializers.SlugField(max_length=255)
    file = serializers.ImageField()

    def validate_file(self, value):
        if value.size > settings.UPLOAD_MAX_FILE_SIZE_BYTES:
            raise serializers.ValidationError("File exceeds allowed size.")

        if value.content_type not in settings.UPLOAD_ALLOWED_IMAGE_MIME_TYPES:
            raise serializers.ValidationError("Unsupported file type.")

        return value
