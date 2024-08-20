import grpc

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grpsapp import sports_pb2
from grpsapp import sports_pb2_grpc


def run():
    # Создаем канал для подключения к серверу
    with grpc.insecure_channel('localhost:50051') as channel:
        # Создаем клиента
        stub = sports_pb2_grpc.SportsLinesStub(channel)

        # Формируем запрос
        request_iterator = iter([
            sports_pb2.SportsLinesRequest(sports=["soccer"], interval=3)
        ])

        # Отправляем запросы и обрабатываем ответы
        try:
            for response in stub.SubscribeOnSportsLines(request_iterator):
                print(f"Received sports lines: {response.lines}")
        except grpc.RpcError as e:
            print(f"gRPC error: {e}")


if __name__ == '__main__':
    run()

# python grpc_client.py
