import csv
import datetime
class customer:

    def __init__(self, name="", cnic="",password="", amount=""):
        self.name = name
        self.cnic = str(cnic)
        self.password = str(password)
        self.amount = str(amount)

    def ShowData(self):
        print(self.name+" ,"+str(self.cnic)+" ,"+str(self.amount)+"\n")

    def add_amount(self,amount1):
        self.amount = self.amount + amount1

    def withdraw_amount(self,amount1):
        self.amount = self.amount - amount1

    def createAccount(self):
        self.name = input("Enter Your Name")
        self.cnic = input("Enter Your CNIC")
        self.password = input("Enter Your Password")
        self.amount = "0"

        filename = "LoginData.csv"
        with open(filename, 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([self.name, self.cnic, self.password, self.amount])


    def search(self, name, password):
        with open('LoginData.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 0:
                    if row[0] == name and row[2] == password:
                        return True
            return False


    def checkbalance(self,name,password):
        with open('LoginData.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 0:
                    if row[0] == name and row[2] == password:
                        print("Your balance is  : " + row[3] + "\n")

    def addamount(self,name,password,amount):
        with open('LoginData.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 0:
                    if row[0] == name and row[2] == password:
                        self.updateAmopunt(name,password,int(amount)+int(row[3]),"Amount Add")

    def updateAmopunt(self, name, password, amount, type):
        with open('LoginData.csv', 'r') as file:
            reader = csv.reader(file)
            with open('temporaryfile.csv', 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                for row in reader:
                    if len(row) > 0:
                        if row[0] == name and password == row[2]:
                            csvwriter.writerow([row[0], row[1], row[2], str(amount)])
                        else:
                            csvwriter.writerow([row[0], row[1], row[2], row[3]])

        with open('temporaryfile.csv', 'r') as file1:
            reader = csv.reader(file1)
            with open('LoginData.csv', 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                for row in reader:
                    if len(row) > 0:
                        csvwriter.writerow([row[0], row[1], row[2], row[3]])

        with open('transaction.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([name, type, datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')])

    def payBills(self, name, password):
        billnumber = input("Enter Bill Number : ")
        amount = int(input("Enter amount"))
        with open('LoginData.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 0:
                    if row[0] == name and row[2] == password:
                        if int(row[3]) >= amount:
                            self.updateAmopunt(name,password,int(row[3])-amount, "Bill Pay")
                            print("Bill is payed.")
                            self.newpage(name, password)
                        else:
                            print("Your Account Balance Is Insufficient......")
                            self.newpage(name,password)


    def withdrawbalance(self, name, password):

        amount = int(input("Enter amount"))
        with open('LoginData.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 0:
                    if row[0] == name and row[2] == password:
                        if int(row[3]) >= amount:
                            x = int(row[3]) - amount
                            self.updateAmopunt(name,password,x, "amount withdrawn")
                            print("Balance is withdrawn.")
                            self.newpage(name,password)
                        else:
                            print("Your Account Balance Is Insufficient......")
                            self.newpage(name,password)



    def newpage(self,name, password):
        print("1. check balance\n2. pay bills\n3. add balance\n4. withdraw balance\n5. Logout")
        option = input("Select a option")
        if option == "1" :
            self.checkbalance(name,password)
            self.newpage(name, password)

        elif option == "2":
            self.payBills(name,password)

        elif option == "3":
            amount = input("Enter Amount")
            self.addamount(name,password,amount)
            self.newpage(name,password)

        elif option == "4":
            self.withdrawbalance(name,password)

        elif option == "5":
            self.page1()



    def login(self):
        name = input("Enter Your Name")
        password = input("Enter Your Password")
        word = self.search(name,password)
        if word == True:
            self.newpage(name, password)
        else:
            print("You have Enter incorrect user name or password.......")
            self.page1()



    @staticmethod
    def page1():
        print("1. Open a Account\n2. Login\n3. Exit")
        option = input()
    # while option != '1' or option != '2':
    #     # system('cls')
    #     option = input()

        if option == "1":
            new_customer = customer()
            new_customer.createAccount()
            input("press Any key to go to main page")
            customer.page1()
        elif option == "2":
            new_customer = customer()
            new_customer.login()
        elif option == "3":
            pass


customer.page1()
