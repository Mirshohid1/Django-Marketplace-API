import logging

from django.db import connection
from django.http import JsonResponse

logger = logging.getLogger("django")


def health_live(request):
    try:
        return JsonResponse({"status": "ok"})
    except Exception:
        logger.exception("Health live failed")
    else:
        logger.info("Health live success")


def health_ready(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_status = "ok"
    except Exception:
        db_status = "fail"
        logger.exception("Health ready failed")

    status = 200 if db_status == "ok" else 503

    logger.info(f"Health ready {db_status}")

    return JsonResponse(
        {
            "status": "ok" if status == 200 else "fail",
            "db": db_status,
        },
        status=status,
    )
