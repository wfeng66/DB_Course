import pymongo
from pymongo.errors import ConnectionFailure
import datetime


class acmeCustomer:
    def __init__(self):
        try:
            client = pymongo.MongoClient('localhost', 27017)
            print("Connected")
        except ConnectionFailure as e:
            print("Connection Failure", e)
        self.client = client
        self.db = client.acme
        self.customer = self.db.customer
        self.account = self.db.account
        self.tran = self.db.tran

    def newcustomer(self, fname, lname, ssn):
        state = input("Your state: ")
        city = input("Your city: ")
        add = input("Your address: ")
        zipcode = int(input("Your zip code: "))
        if self.db.customer.count_documents({'ssn': ssn}) > 0:
            print("You already have an account!")
            return 0
        else:
            maxid_cur = self.customer.find().sort('_id', pymongo.DESCENDING).limit(1)
            for row in maxid_cur:
                self.maxid = row['_id']
            try:
                self.customer.insert_one({'_id': (self.maxid+1), 'fn': fname, 'ln': lname, 'ssn': ssn, 'add': add,
                                      'city': city, 'state': state, 'zip': zipcode})
                self.maxid = self.maxid +1
                print("Congratulation! New user has been created!")
                print("What kind of account you want?")
                acckind = int(input("(1. Checking account   2. Saving account   3. Both)"))
                if acckind == 1:
                    self.newaccount(ssn, "C")
                elif acckind == 2:
                    self.newaccount(ssn, "S")
                elif acckind == 3:
                    self.newaccount(ssn, "B")
            except ConnectionFailure as e:
                print("Creating new user failure", e)

    def newaccount(self, ssn, acckind):
        accid_cur = self.account.find().sort('_id', pymongo.DESCENDING).limit(1)
        for row in accid_cur:
            accid = row['_id']
        cusid_cur = self.customer.find({"ssn": ssn}, {"_id": 1})
        for row in cusid_cur:
            cus_id = row['_id']
        nowtime = datetime.datetime.now().timestamp()
        if acckind == "S":
            accno_cur = self.account.find({"acctype": "S"}).sort('_id', pymongo.DESCENDING).limit(1)
            for row in accno_cur:
                accno = row['accno']

            self.account.insert_one({"_id": (accid+1), "cus_id": cus_id, "accno": (accno+1), "acctype": "S",
                                    "intrate": 0.018, "overrate": 25, "bln": 0, "lastaccess": nowtime})
        elif acckind == "C":
            accno_cur = self.account.find({"acctype": "C"}).sort('_id', pymongo.DESCENDING).limit(1)
            for row in accno_cur:
                accno = row['accno']
            self.account.insert_one({"_id": (accid + 1), "cus_id": cus_id, "accno": (accno + 1), "acctype": "C",
                                    "intrate": 0.0, "overrate": 25, "bln": 0, "lastaccess": nowtime})
        elif acckind == "B":
            chkno_cur = self.account.find({"acctype": "C"}).sort('_id', pymongo.DESCENDING).limit(1)
            for row in chkno_cur:
                chkno = row['accno']
            svgno_cur = self.account.find({"acctype": "S"}).sort('_id', pymongo.DESCENDING).limit(1)
            for row in svgno_cur:
                svgno = row['accno']
            self.account.insert_one({"_id": (accid+1), "cus_id": cus_id, "accno": (svgno+1), "acctype": "S",
                                    "intrate": 0.018, "overrate": 25, "bln": 0, "lastaccess": nowtime})
            self.account.insert_one({"_id": (accid + 2), "cus_id": cus_id, "accno": (chkno + 1), "acctype": "C",
                                    "intrate": 0.0, "overrate": 25, "bln": 0, "lastaccess": nowtime})
        print("Your account was created !")

    def checkbln(self,accno):
        try:
            bln_cur = self.account.find({"accno":accno},{"bln":1, "_id": 0})
            for row in bln_cur:
                balance = row['bln']
        except ConnectionFailure as e:
            print("Access database fail: ", e)
        nowtime = datetime.datetime.now().timestamp()
        self.account.update_one({"accno": {"$eq": accno}}, {"$set": {"lastaccess": nowtime}})
        return balance

    def showhist(self, accno):
        try:
            hist_cur = self.tran.find({"accno": accno})
            for row in hist_cur:
                print(row)
            print("Finish!")
        except ConnectionFailure as e:
            print("Access database fail: ", e)
        nowtime = datetime.datetime.now().timestamp()
        self.account.update_one({"accno": {"$eq": accno}}, {"$set": {"lastaccess": nowtime}})

    def deposit(self, accno, amt):
        if self.account.count_documents({"cus_id": self.cusid, "accno": accno})>0:
            bln_cur = self.account.find({"accno":{"$eq": accno}},{"bln":1, "_id": 0})
            for row in bln_cur:
                balance = row['bln']
            balance = balance + amt
            nowtime = datetime.datetime.now().timestamp()
            self.account.update_one({"accno": {"$eq": accno}}, { "$set":{"bln": balance, "lastaccess": nowtime}})
            tranid_cur = self.tran.find().sort('_id', pymongo.DESCENDING).limit(1)
            for row in tranid_cur:
                tranid = row['_id']
            tranid = tranid +1
            self.tran.insert_one({"_id": tranid, "cus_id": self.cusid, "accno": accno, "trantype": "D",
                                  "amt": amt, "relacc": 0, "createdon": nowtime})
            print("Deposit successful!")
        else:
            print("Sorry! You haven't this account, please verify!")

    def withdraw(self, accno, amt):
        if self.account.count_documents({"cus_id": self.cusid, "accno": accno})>0:
            bln_cur = self.account.find({"accno":{ "$eq": accno}},{"bln":1, "overrate": 1, "_id": 0})
            for row in bln_cur:
                balance = row['bln']
                overfee = row['overrate']
            if balance == 0:
                balance = balance - overfee
            if balance - amt >= 0:
                balance = balance - amt
            else:
                print("Sorry！Your balance is not enough, only %.2f" % balance)
                return 0
            nowtime = datetime.datetime.now().timestamp()
            self.account.update_one({"accno": { "$eq": accno}}, { "$set":{"bln": balance, "lastaccess": nowtime}})
            tranid_cur = self.tran.find().sort('_id', pymongo.DESCENDING).limit(1)
            for row in tranid_cur:
                tranid = row['_id']
            tranid = tranid +1
            self.tran.insert_one({"_id": tranid, "cus_id": self.cusid, "accno": accno, "trantype": "W",
                                  "amt": amt, "relacc": 0, "createdon": nowtime})
            print("Withdraw successful!")
        else:
            print("Sorry! You haven't this account, please verify!")

    def setup(self, fname, lname, ssn):
        cus_cur = self.customer.find({"ssn": {"$eq":ssn}}, {"_id": 1,"fn": 1, "ln": 1})
        for row in cus_cur:
            self.cusid = row['_id']
            self.fn = row['fn']
            self.ln = row['ln']
        if self.fn == fname and self.ln == lname:
            print("Thanks your cooperation!")
        else:
            print("Sorry! Your information does not match our system!")


def main():
    print("Welcome!\nMAy I help you?\n")
    print("(1.new customer 2.open new account 3. deposit 4. withdraw 5. check balance 6.check history)\n")
    op = int(input("Please enter the input: "))
    fn = input("Your first name: ")
    ln = input("Your last name: ")
    ssn = int(input("Your SSN, please!"))
    if op == 1:
        newclient = acmeCustomer()
        newclient.newcustomer(fn, ln, ssn)
        newclient.client.close()
        return
    elif op == 2:
        acckind = int(input("Please select the kind of account: (1. Saving   2. Checking   3. Both)"))
        currclient = acmeCustomer()
        if acckind == 1:
            currclient.newaccount(ssn, "S")
        elif acckind == 2:
            currclient.newaccount(ssn, "C")
        elif acckind == 3:
            currclient.newaccount(ssn, "B")
        currclient.client.close()
    elif op == 3:
        accno = int(input("Which account do you want to deposit?"))
        amt = int(input("How much you want to deposit?"))
        currclient = acmeCustomer()
        currclient.setup(fn,ln,ssn)
        currclient.deposit(accno, amt)
    elif op == 4:
        accno = int(input("Which account do you want to withdraw from?"))
        amt = int(input("How much you want to withdraw?"))
        currclient = acmeCustomer()
        currclient.setup(fn, ln, ssn)
        currclient.withdraw(accno, amt)
    elif op == 5:
        currclient = acmeCustomer()
        currclient.setup(fn, ln, ssn)
        accno = int(input("Which account do you want to check?"))
        bln = currclient.checkbln(accno)
        print("The balance of %d is %.2f." % (accno, bln))
    elif op == 6:
        currclient = acmeCustomer()
        currclient.setup(fn, ln, ssn)
        accno = int(input("Which account do you want to check?"))
        currclient.showhist(accno)
    currclient.client.close()


if __name__ == "__main__":
    main()
