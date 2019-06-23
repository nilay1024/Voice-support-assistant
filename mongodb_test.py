import pymongo
from pprint import pprint

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["payment_data"]

# insert_more = 'y'
# while insert_more == 'y':
# 	name = input("Customer name: ")
# 	date = input("Last payment date: [dd-mm-yy]: ")
# 	amount = input("Bill amount: ")
# 	mode = input("Mode: ")
# 	success = input("success/failure?: ")
# 	status = input("Service status: ")
# 	mydict = {"CustName": name, "LastPaymentDate": date, "Amount": amount, "Mode": mode, "Success/Failure": success, "Status": status}
# 	insert_doc = mycol.insert_one(mydict)
# 	print("Document inserted successfully with inserted_id: ", insert_doc.inserted_id)
# 	insert_more = input("Insert more data? [y/n]: ")


def bill_payment_status():
	payment_mode = input("Enter payment mode")
	amount = input("Enter paid amount")
	date = input("Enter date of payment")
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["mydatabase"]
	mycol = mydb["payment_data"]
	result = mycol.find({'Amount': amount, 'Mode': payment_mode, 'LastPaymentDate': date})
	if result.count() >= 1:
		print("Entry found ", result.count())
		print(result[0])
	else:
		print("Entry not found")


# print("\nCollection after insertion:\n")

# # SIMILAR TO SELECT * IN POSTGRES/MYSQL
# result = mycol.find()
# for i in result:
# 	pprint(i)
# 	print()

bill_payment_status()
