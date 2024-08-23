import json
import threading
# для создания пула потоков, который управляет асинхронным выполнением
from concurrent import futures
import time
import os
import logging
import requests


import django
import grpc
from grpsapp import sports_pb2_grpc

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SoftPro.settings')
django.setup()
from httpapp.models import Soccer, Baseball, Football

from . import sports_pb2 as sports__pb2

logging.basicConfig(level=logging.INFO)


class SportsLinesService(sports_pb2_grpc.SportsLinesServicer):
    """
    Контекст gRPC, предоставляющий метаданные и вспомогательные методы для обработки запроса
    Запрос: [soccer, football] 3s
    Ответ: {soccer: 1.13, football: 2.19}
    """

    def __init__(self, stop_event):
        self.first_request = True  # отслеживает, был ли уже выполнен первый запрос
        self.previous_lines = {}  # словарь предыдущих значений линий спортов
        self.stop_event = stop_event  # отслеживает запрос от клиента и останавливает воркеров

    def SubscribeOnSportsLines(self, request_iterator, context):
        """
        Обрабатывает входящие запросы и отправляет обратно потоки данных клиентам
        """
        logging.info('Start SubscribeOnSportsLines')
        if not self.stop_event.is_set():
            self.stop_event.set()

        # Итератор входящих запросов, позволяющий обрабатывать потоковые запросы
        for request in request_iterator:
            sports_lines = self.get_sports_lines(request.sports)
            yield sports__pb2.SportsLinesResponse(lines=sports_lines)
            while True:
                sports_lines = self.get_sports_lines(request.sports)
                yield sports__pb2.SportsLinesResponse(lines=sports_lines)

                # Проверяем на отмену (если клиент отключается)
                if context.is_active():
                    time.sleep(request.interval)
                else:
                    break

    def get_sports_lines(self, sports):
        """
        Реализация основного функционала - получение линий для указанных спортов
        в соответствии с заданным интервалом и сохранение их в базе данных
        """
        # Получает последние данные о линиях для указанных видов спорта
        result = {}
        for sport in sports:
            url = f'http://lines_provider:8000/api/v1/lines/{sport}'
            logging.info('GET request %s', url)
            response = requests.get(url, timeout=10)

            response_data = json.loads(response.content)
            logging.info('Response data: %s', response_data)
            value_str = response_data['lines'][sport.upper()]
            current_value = float(f"{float(value_str):.2f}")

            if self.first_request:
                result[sport] = current_value
            else:
                result[sport] = current_value - self.previous_lines[sport]

            self.previous_lines[sport] = current_value

            if sport == 'soccer':
                Soccer.objects.create(line=current_value)
            elif sport == 'football':
                Football.objects.create(line=current_value)
            elif sport == 'baseball':
                Baseball.objects.create(line=current_value)
            else:
                logging.critical('sport not supported')
                return {'error': 'an incorrect sport'}

        self.first_request = False
        logging.debug('Result is %s', result)
        return result


def start_worker(sport, interval, stop_event):
    """
    Первоначальный старт воркеров для синхронизации линий раз в минуту
    пока не поступит запрос хотя бы от одного клиента
    """
    while not stop_event.is_set():
        response = requests.get(f'http://lines_provider:8000/api/v1/lines/{sport}', timeout=10)
        response_data = json.loads(response.content)
        current_value = float(response_data['lines'][sport.upper()])
        if sport == 'soccer':
            Soccer.objects.create(line=current_value)
        elif sport == 'football':
            Football.objects.create(line=current_value)
        elif sport == 'baseball':
            Baseball.objects.create(line=current_value)
        time.sleep(interval)


def serve():
    """
    Запуск первоначальной синхронизации и gRPC сервера
    """

    # Создаем события остановки для воркеров
    stop_event = threading.Event()

    # Список спортов и интервалов для воркеров
    sports_intervals = [("soccer", 60), ("football", 60), ("baseball", 60)]

    logging.info('First start workers for a synchronization')
    # Запуск воркеров в отдельных потоках
    for sport, interval in sports_intervals:
        threading.Thread(target=start_worker, args=(sport, interval, stop_event)).start()

    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=3))  # Использует пул потоков для обработки нескольких запросов одновременно
    # регистрирует сервис на сервере
    sports_pb2_grpc.add_SportsLinesServicer_to_server(SportsLinesService(stop_event), server)
    logging.info('Listening on port 50051')
    server.add_insecure_port('[::]:50051')  # Сервер слушает на порту 50051
    logging.info('Start server')
    server.start()  # Сервер начинает обрабатывать входящие запросы
    server.wait_for_termination()  # Сервер остается активным, пока его не остановят


if __name__ == '__main__':
    serve()
