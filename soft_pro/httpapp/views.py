from datetime import datetime

from django.http import JsonResponse
from django.db import connection, OperationalError
from .models import Soccer, Baseball, Football


def check_db_connection():
    """
    Метод проверки соединения с базой данных
    """
    try:
        connection.ensure_connection()
        return True
    except OperationalError:
        return False


def check_first_sync_complete():
    """
    Метод проверки синхронизации базы данных
    """
    date = datetime.now().strftime('%Y-%m-%d')
    return (Soccer.objects.filter(date=date).exists()  # pylint: disable=no-member
            and Baseball.objects.filter(date=date).exists()  # pylint: disable=no-member
            and Football.objects.filter(date=date).exists())  # pylint: disable=no-member


def ready(request):
    """
    View-функция, позволяющая проверить соединение с базой данных
    и синхронизацию
    """
    db_ready = check_db_connection()
    first_sync_complete = check_first_sync_complete()

    if db_ready and first_sync_complete:
        return JsonResponse({"status": "ready"}, status=200)
    return JsonResponse({"status": "not ready"}, status=503)
