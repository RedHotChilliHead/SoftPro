from django.http import JsonResponse
from django.db import connection


def ready(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "ok"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "details": str(e)}, status=500)
