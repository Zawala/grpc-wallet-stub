import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27010/")
mydb = myclient["grpcwallets"]
mycol = mydb["customers"]




class wallet_users():
    def credit_user(username,amount, type):

        myquery = { "username": username }
        newvalues = { "$set": { f"{type}": amount } }
        mycol.update_one(myquery, newvalues)
        


    def debit_user(username, amount,type):
        pass

    def get_balance(username):
        myquery = { "username": username }
        mydoc = mycol.find(myquery)
        return mydoc

    def add_user(amount,username):
        user={'username':username, 'balance':{
            'voip':amount,
            'monetary':0

        }
        }