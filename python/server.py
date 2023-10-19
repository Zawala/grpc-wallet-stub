import grpc
from concurrent import futures
import time
from mongo_interface import wallet_user
from databank import (wallet_pb2, wallet_pb2_grpc)

class walletServicer(wallet_pb2_grpc.walletServicer):
    def credit(self,user, context):
        print(user)
        reply =  wallet_pb2.reply()
        requested_user=wallet_user(user.username)
        if user.voip:
            print(1)
            balance=requested_user.credit_user('voip', user.voip)
            reply.voip= balance['voip']
            reply.monetary= balance['monetary']
        elif user.monetary:
            print(2)
            balance=requested_user.credit_user('monetary', user.monetary)
            reply.voip= balance['voip']
            reply.monetary= balance['monetary']
        else:
            reply.info='Error Request'
            
        return reply

    def debit(self,user, context):
        reply =  wallet_pb2.reply()
        requested_user=wallet_user(user.username)
        if user.voip:
            balance=requested_user.debit_user('voip', user.voip)
            reply.voip= balance['voip']
            reply.monetary= balance['monetary']
        elif user.monetary:
            balance=requested_user.debit_user('monetary', user.monetary)
            reply.voip= balance['voip']
            reply.monetary= balance['monetary']
        else:
            reply.info='Error Request'
            
        return reply

    def balance(self,user, context):
        reply =  wallet_pb2.reply()
        requested_user=wallet_user(user.username)
        balance=requested_user.get_balance()
        print(2, balance)
        reply.voip= float(balance['voip'])
        reply.monetary= float(balance['monetary'])
        return reply
    

    def add_user(self,user, context):
        reply =  wallet_pb2.reply()
        requested_user=wallet_user(user.username)
        reply.info=requested_user.add_user()
        return reply
    
    

    def remove_user(self,user, context):
        reply =  wallet_pb2.reply()
        requested_user=wallet_user(user.username)
        reply.info=requested_user.delete_user()
        return reply



def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # use the generated function `add_CalculatorServicer_to_server`
    # to add the defined class to the server
    wallet_pb2_grpc.add_walletServicer_to_server(
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