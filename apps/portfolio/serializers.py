from rest_framework import serializers

from apps.core.serializers import LinkSerializer
from apps.portfolio.models import Project, ProjectImage, ProjectMetric, Service


class ServiceSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = (
            "id",
            "slug",
            "title",
            "summary",
            "long_description",
            "icon_key",
            "features",
            "tech_stack",
            "challenges_vs_solutions",
            "my_services",
            "development_process",
            "links",
        )


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ("id", "image_url", "title", "sort_order")


class ProjectMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMetric
        fields = ("id", "label", "value", "sort_order")


class ProjectListSerializer(serializers.ModelSerializer):
    image_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "slug",
            "title",
            "subtitle",
            "description",
            "tech_stack",
            "period",
            "live_url",
            "github_url",
            "category",
            "role",
            "is_open_source",
            "is_featured",
            "thumbnail_image_url",
            "image_count",
        )


class ProjectDetailSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    metrics = ProjectMetricSerializer(many=True, read_only=True)
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "slug",
            "title",
            "subtitle",
            "description",
            "abstract",
            "tech_stack",
            "user_roles",
            "security",
            "references",
            "period",
            "live_url",
            "github_url",
            "category",
            "role",
            "quote",
            "problem_statement",
            "challenges",
            "solutions",
            "feature_items",
            "technical_architecture",
            "impact_metrics",
            "is_open_source",
            "is_featured",
            "thumbnail_image_url",
            "images",
            "metrics",
            "links",
        )
