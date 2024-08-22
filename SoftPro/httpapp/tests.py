from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from httpapp.views import ready
from httpapp.models import Baseball, Football, Soccer


class ReadyTestCase(TestCase):
    def setUp(self):
        self.baseball = Baseball.objects.create(line=1.1)
        self.football = Football.objects.create(line=1.2)
        self.soccer = Soccer.objects.create(line=1.3)

    def tearDown(self):
        self.baseball.delete()
        self.football.delete()
        self.soccer.delete()

    def test_ready(self):
        """
        Проверка статуса готовности базы данных
        """
        response = self.client.get(reverse('httpapp:ready'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"status": "ready"}')


class NotReadyTestCase(TestCase):
    @patch('httpapp.views.check_db_connection')
    def test_not_ready(self, mock_check_db_connection):
        """
        Проверка статуса не готовности базы данных
        """
        response = self.client.get(reverse('httpapp:ready'))
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.content, b'{"status": "not ready"}')

        # Мокируем разорванное соединение
        mock_check_db_connection.return_value = False
        response = ready(request=None)
        self.assertEqual(response.content, b'{"status": "not ready"}')
