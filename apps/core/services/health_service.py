from django.db import connection
from django.db.utils import DatabaseError, OperationalError


def get_health_payload() -> tuple[dict[str, str], int]:
    db_state = "connected"
    status_text = "ok"
    status_code = 200

    # why: Executing a query validates real DB connectivity, not just TCP reachability.
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except (OperationalError, DatabaseError):
        db_state = "disconnected"
        status_text = "degraded"
        status_code = 503

    return {"status": status_text, "database": db_state}, status_code
