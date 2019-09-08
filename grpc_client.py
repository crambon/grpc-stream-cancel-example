from concurrent import futures

import grpc
import message_pb2
import message_pb2_grpc


def stream(stub, key, key_stack):
    # _Rendezvousオブジェクトを受け取る
    responses = stub.Stream(message_pb2.Request(key=key))
    for res in responses:
        if key not in key_stack:
            responses.cancel()
            # これでもいい
            # res.cancel()
    key_stack.discard(key)


def run():
    executor = futures.ThreadPoolExecutor(max_workers=10)
    key_stack = set()
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = message_pb2_grpc.MessageStub(channel)
        while True:
            print('Stacking keys: {}'.format(key_stack))
            user_input = input('Input key: > ')
            if user_input not in key_stack:
                print('Create stream, key: ', user_input)
                executor.submit(lambda: stream(stub, user_input, key_stack))
                key_stack.add(user_input)
            else:
                print('Cancel stream, key: ', user_input)
                key_stack.discard(user_input)


if __name__ == '__main__':
    run()
