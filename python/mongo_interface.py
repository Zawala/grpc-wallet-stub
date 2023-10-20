import pymongo
from databank import wallet_pb2_grpc, wallet_pb2
import grpc

try: 
    myclient = pymongo.MongoClient("mongodb://0.0.0.0:27010/")
    mydb = myclient["grpcwallets"]
    mycol = mydb["customers"]
except Exception as e:
    raise (f"Could not connect to server: {e}")



class wallet_user():

    def __init__(self,username):
        self.username=username

    def credit_user(self, type, amount):
        myquery = { "username": self.username }
        try:
            old_wallet = mycol.find(myquery)
            for wallet in old_wallet:
                new_amount= float(wallet['balance'][f'{type}']+amount)
                newvalues = { "$set": { f'balance.{type}': new_amount } }
                mycol.update_one(myquery, newvalues)
                # Fetch the updated wallet
                updated_wallet = mycol.find(myquery)
                for wallet in updated_wallet:
                    # Add a success message to the info field of the returned balance
                    wallet_copy = wallet['balance'].copy()
                    wallet_copy['info'] = 'Transaction successful'
                    return wallet_copy
        except Exception as e:
            # Add the exception message to the info field of the returned balance
            return {'info': f"{e}"}

    def debit_user(self, type, amount):
        myquery = { "username": self.username }
        try:
            old_wallet = mycol.find(myquery)
            for wallet in old_wallet:
                current_balance = float(wallet['balance'][f'{type}'])
                if current_balance < amount:
                    wallet_copy = wallet['balance'].copy()
                    wallet_copy['info'] = 'Insufficient funds'
                    return wallet_copy
                else:
                    new_amount = current_balance - amount
                    newvalues = { "$set": { f'balance.{type}': new_amount } }
                    mycol.update_one(myquery, newvalues)
                    updated_wallet = mycol.find(myquery)
                    for wallet in updated_wallet:
                        wallet_copy = wallet['balance'].copy()
                        wallet_copy['info'] = 'Transaction successful'
                        return wallet_copy
        except Exception as e:
            return f"{e}"
        

    def get_balance(self):
        myquery = { "username": self.username }
        updated_wallet = mycol.find(myquery)
        for wallet in updated_wallet:
            return wallet['balance']
        
    def add_user(self):
        try:
            myquery = { "username": self.username }      
            if not mycol.count_documents(myquery) > 0:
                user={'username':self.username, 'balance':{
                'voip':0,
                'monetary':0
                }
                }
                x = mycol.insert_one(user)
                return 'Success'
            else:
                return 'Already Exists'
        except Exception as e:
            return e
        
    def delete_user(self):
        try:
            myquery = { "username": self.username }
            x = mycol.delete_one(myquery)
            if x.deleted_count>0:
             return 'Success'
            else:
                return 'Error 404'
        except Exception as e:
            return e
 