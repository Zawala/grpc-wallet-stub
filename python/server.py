import grpc
from concurrent import futures
import time
from .databank import (wallet_pb2, wallet_pb2_grpc)

class walletServicer(wallet_pb2_grpc.wallet__pb2):
    def credit(self,request, context):
        response =  wallet_pb2.reply()
        response.reply= users.display(request.name)
        return response

    def debit(self,request, context):
        response =  wallet_pb2.reply()
        response.value= users.delete(request.name)
        return response

    def balance(self,request, context):
        response =  wallet_pb2.reply()
        response.value= users.add(request.name, request.address)
        return response



def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # use the generated function `add_CalculatorServicer_to_server`
    # to add the defined class to the server
    wallet_pb2.add_usersServicer_to_server(
            walletServicer(), server)

        # listen on port 50051
    print('Starting server. Listening on port 50051.')
    server.add_insecure_port('[::]:50051')
    server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run()