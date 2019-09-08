import time
from concurrent import futures

import grpc
import message_pb2
import message_pb2_grpc


class MessageServicer(message_pb2_grpc.MessageServicer):
    def Stream(self, request, context):
        for i in range(1, 11):
            time.sleep(1)
            message = 'key: {}, progress: {}'.format(request.key, '+' * i)
            print(message)
            yield message_pb2.Response(message=message)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_MessageServicer_to_server(
        MessageServicer(),
        server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Server started !')
    try:
        while True:
            time.sleep(24 * 60 * 60)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
