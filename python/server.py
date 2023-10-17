import grpc
from concurrent import futures
import time
from grpc_gen import (users_pb2_grpc,users_pb2)
from function import users

class UserServicer(users_pb2_grpc.usersServicer):
    def display(self,request, context):
        response =  users_pb2.response()
        response.reply= users.display(request.name)
        return response

    def delete(self,request, context):
        response =  users_pb2.response()
        response.value= users.delete(request.name)
        return response

    def add(self,request, context):
        response =  users_pb2.response()
        response.value= users.add(request.name, request.address)
        return response



def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # use the generated function `add_CalculatorServicer_to_server`
    # to add the defined class to the server
    users_pb2_grpc.add_usersServicer_to_server(
            UserServicer(), server)

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