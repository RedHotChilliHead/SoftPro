import json
import threading
from concurrent import futures
from unittest.mock import patch, MagicMock

import grpc

from django.test import TestCase
from django.db import connection

from grpsapp import sports_pb2_grpc, sports_pb2
from grpsapp.grpc_server import SportsLinesService


class GRPCTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Метод для установки gRPC сервера перед запуском всех тестов
        """
        cls.stop_event = threading.Event()

        # Запускаем gRPC сервер в отдельном потоке
        cls.server_thread = threading.Thread(target=cls.start_grpc_server)
        cls.server_thread.start()

        # Устанавливаем соединение с сервером
        cls.channel = grpc.insecure_channel('localhost:50051')
        cls.stub = sports_pb2_grpc.SportsLinesStub(cls.channel)

    @classmethod
    def start_grpc_server(cls):
        """
        Метод для запуска gRPC сервера
        """
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
        sports_pb2_grpc.add_SportsLinesServicer_to_server(SportsLinesService(cls.stop_event), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        cls.server = server
        server.wait_for_termination()

    @classmethod
    def tearDownClass(cls):
        """
        Метод для остановки gRPC сервера после выполнения всех тестов
        """
        cls.stop_event.set()
        cls.channel.close()
        if hasattr(cls, 'server'):
            cls.server.stop(0)
        if hasattr(cls, 'server_thread'):
            cls.server_thread.join(timeout=5)

        # Закрытие всех открытых соединений с базой данных
        connection.close()

        # Попробуйте закрыть все активные соединения (с осторожностью)
        with connection.cursor() as cursor:
            cursor.execute("""
                    SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE pg_stat_activity.datname = current_database()
                    AND pid <> pg_backend_pid();
                """)

    @patch('grpsapp.grpc_server.requests.get')
    def test_subscribe_on_sports_lines(self, mock_get):
        """
        Тестирование метода SubscribeOnSportsLines
        """
        # Настраиваем mock для requests.get
        mock_response = MagicMock()
        mock_response.content = json.dumps({
            'lines': {
                'SOCCER': '1.13',
                'FOOTBALL': '2.19'
            }
        }).encode('utf-8')
        mock_get.return_value = mock_response

        request = sports_pb2.SportsLinesRequest(sports=['soccer', 'football'], interval=1)
        response_iterator = self.stub.SubscribeOnSportsLines(iter([request]))

        # Получаем первый ответ
        response = next(response_iterator)
        self.assertIn('soccer', response.lines)
        self.assertAlmostEqual(response.lines['soccer'], 1.13, places=2)
        self.assertIn('football', response.lines)
        self.assertAlmostEqual(response.lines['football'], 2.19, places=2)

        # Проверяем, что метод get был вызван с правильными аргументами
        mock_get.assert_any_call('http://lines_provider:8000/api/v1/lines/soccer', timeout=10)
        mock_get.assert_any_call('http://lines_provider:8000/api/v1/lines/football', timeout=10)
