from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def unified_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return Response(
            {
                "success": False,
                "message": "Internal server error.",
                "errors": {},
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if isinstance(exc, ValidationError):
        message = "Validation error."
        errors = response.data
    else:
        detail = response.data.get("detail") if isinstance(response.data, dict) else None
        message = str(detail) if detail else "Request failed."
        errors = response.data if isinstance(response.data, dict) else {"detail": response.data}

    response.data = {
        "success": False,
        "message": message,
        "errors": errors,
    }
    return response