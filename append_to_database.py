import pymongo
from pprint import pprint

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["payment_data"]

insert_more = 'y'
while insert_more == 'y':
	name = input("Customer name: ")
	date = input("Last payment date: [dd-mm-yy]: ")
	amount = input("Bill amount: ")
	mode = input("Mode: ")
	success = input("success/failure?: ")
	status = input("Service status: ")
	mydict = {"CustName": name, "LastPaymentDate": date, "Amount": amount, "Mode": mode, "Success/Failure": success, "Status": status}
	insert_doc = mycol.insert_one(mydict)
	print("Document inserted successfully with inserted_id: ", insert_doc.inserted_id)
	insert_more = input("Insert more data? [y/n]: ")


print("\nCollection after insertion:\n")

# SIMILAR TO SELECT * IN POSTGRES/MYSQL
result = mycol.find()
for i in result:
	pprint(i)
	print()
