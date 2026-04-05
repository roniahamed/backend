import cloudinary.uploader
from django.core.exceptions import ValidationError

from apps.portfolio.models import Project
from apps.portfolio.tasks import optimize_project_cover_task


def upload_project_cover_and_enqueue(*, project_slug: str, image_file) -> dict[str, str]:
    project = Project.objects.filter(slug=project_slug, is_published=True).only("id", "slug").first()
    if project is None:
        raise ValidationError("Project not found for provided slug.")

    upload_result = cloudinary.uploader.upload(
        image_file,
        folder=f"portfolio/projects/{project.slug}",
        resource_type="image",
    )

    secure_url = upload_result.get("secure_url")
    public_id = upload_result.get("public_id")
    if not secure_url or not public_id:
        raise ValidationError("Cloudinary upload returned incomplete metadata.")

    project.thumbnail_image_url = secure_url
    project.save(update_fields=["thumbnail_image_url"])

    optimize_project_cover_task.delay(project.id, public_id)
    return {"thumbnail_image_url": secure_url, "public_id": public_id}
