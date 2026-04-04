from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.blog.models import BlogPost, Tag
from apps.portfolio.models import Project, ProjectImage, Service


def build_user(email: str = "owner@example.com"):
    user_model = get_user_model()
    return user_model.objects.create_user(
        username="owner",
        email=email,
        password="pass1234!",
        full_name="Roni Ahamed",
    )


def test_health_endpoint_returns_ok(db):
    client = APIClient()

    response = client.get("/api/v1/health/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] == "ok"


def test_public_profile_endpoint_returns_latest_public_profile(db):
    user_model = get_user_model()
    user_model.objects.create_user(
        username="hidden",
        email="hidden@example.com",
        password="pass1234!",
        full_name="Hidden",
        is_public_profile=False,
    )
    public_user = build_user("public@example.com")

    client = APIClient()
    response = client.get("/api/v1/profile/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == public_user.email


def test_projects_endpoint_uses_slug_lookup_and_nested_images(db):
    project = Project.objects.create(
        slug="eastmond-villas",
        title="Eastmond Villas",
        subtitle="Luxury Rental Platform",
        description="Project description",
        abstract="Long abstract",
        tech_stack=["Django REST Framework", "PostgreSQL"],
        user_roles=["Admin"],
        security={"authentication": "JWT"},
        references={"migration": "python manage.py migrate"},
        period="2025-2026",
        category="Full Stack",
        role="Backend",
        quote="A production platform",
        problem_statement="Complex booking sync",
        published_at=timezone.now(),
    )
    ProjectImage.objects.create(project=project, image_url="https://example.com/image.jpg", sort_order=1)

    client = APIClient()
    list_response = client.get("/api/v1/projects/")
    detail_response = client.get(f"/api/v1/projects/{project.slug}/")

    assert list_response.status_code == status.HTTP_200_OK
    assert list_response.data["results"][0]["slug"] == project.slug
    assert detail_response.status_code == status.HTTP_200_OK
    assert len(detail_response.data["images"]) == 1


def test_services_and_blog_endpoints_return_public_records(db):
    service = Service.objects.create(
        slug="api-development",
        title="API Development",
        summary="Build robust APIs",
        long_description="Long form",
        icon_key="Code2",
        features=["JWT auth"],
        tech_stack=["Django REST Framework"],
        sort_order=1,
    )

    author = build_user("blog@example.com")
    tag = Tag.objects.create(name="Django", slug="django")
    post = BlogPost.objects.create(
        slug="shipping-api-design",
        title="Shipping API Design",
        excerpt="How to design clean contracts",
        content="Deep dive content",
        author=author,
        status=BlogPost.STATUS_PUBLISHED,
        published_at=timezone.now(),
    )
    post.tags.add(tag)

    client = APIClient()
    services_response = client.get("/api/v1/services/")
    blog_response = client.get("/api/v1/blog/posts/")

    assert services_response.status_code == status.HTTP_200_OK
    assert services_response.data[0]["slug"] == service.slug
    assert blog_response.status_code == status.HTTP_200_OK
    assert blog_response.data["results"][0]["slug"] == post.slug


def test_contact_submission_validates_message_and_jwt_token_works(db):
    user = build_user()
    client = APIClient()

    invalid_payload = {
        "name": "Roni",
        "email": "hello@example.com",
        "company": "Acme",
        "service_interest": "API Development",
        "message": "Too short",
    }
    invalid_response = client.post("/api/v1/contact/", invalid_payload, format="json")

    assert invalid_response.status_code == status.HTTP_400_BAD_REQUEST

    valid_payload = {**invalid_payload, "message": "I need a backend redesign with observability and docs."}
    valid_response = client.post("/api/v1/contact/", valid_payload, format="json")
    assert valid_response.status_code == status.HTTP_201_CREATED

    token_response = client.post(
        reverse("token-obtain-pair"),
        {"email": user.email, "password": "pass1234!"},
        format="json",
    )
    assert token_response.status_code == status.HTTP_200_OK
    assert "access" in token_response.data
