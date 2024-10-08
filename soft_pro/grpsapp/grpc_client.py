import logging

import sys
import os
import grpc
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grpsapp import sports_pb2
from grpsapp import sports_pb2_grpc


def run():
    logging.basicConfig(level=logging.INFO)
    # Создаем канал для подключения к серверу
    with grpc.insecure_channel('localhost:50051') as channel:
        # Создаем клиента
        stub = sports_pb2_grpc.SportsLinesStub(channel)

        # Формируем запрос
        request_iterator = iter([
            sports_pb2.SportsLinesRequest(sports=["soccer", "football"], interval=6)
        ])

        # Отправляем запросы и обрабатываем ответы
        try:
            for response in stub.SubscribeOnSportsLines(request_iterator):
                logging.info("Received sports lines: %s", response.lines)

        except grpc.RpcError:
            logging.error("gRPC was terminated")


if __name__ == '__main__':
    run()

# python grpc_client.py
