from apps.users.models import User


def get_latest_public_profile() -> User | None:
    return User.objects.filter(is_public_profile=True).only(
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
        "updated_at",
    ).order_by("-updated_at").first()
