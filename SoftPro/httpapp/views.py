from django.http import JsonResponse
from django.db import connection
from .models import Soccer, Baseball, Football

from datetime import datetime


def check_db_connection():
    try:
        connection.ensure_connection()
        return True
    except Exception:
        return False


def check_first_sync_complete():
    date = datetime.now().strftime('%Y-%m-%d')
    return (Soccer.objects.filter(date=date).exists()
            and Baseball.objects.filter(date=date).exists()
            and Football.objects.filter(date=date).exists())


def ready(request):
    db_ready = check_db_connection()
    first_sync_complete = check_first_sync_complete()

    if db_ready and first_sync_complete:
        return JsonResponse({"status": "ready"}, status=200)
    else:
        return JsonResponse({"status": "not ready"}, status=503)

# def ready(request):
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT 1")
#         return JsonResponse({"status": "ok"}, status=200)
#     except Exception as e:
#         return JsonResponse({"status": "error", "details": str(e)}, status=500)
