import mysql.connector
import csv

mydb = mysql.connector.connect(
    host = "localhost",
    passwd = "sql123",
    user="root",
    database="test1"
)
mycursor = mydb.cursor()
with open('LoginData.csv','r') as file:
    reader = csv.reader(file)
    all=[]
    for i in reader:
        if len(i) > 0:
            value = (i[0],i[1],i[2],i[3])
            all.append(value)

    query = "insert into customer (name,cnic,amount,password) values (%s,%s,%s,%s)"
    mycursor.executemany(query, all)
    mydb.commit()

    # mycursor.execute("select * from customer")
    # myresult = mycursor.fetchall()
    # print(myresult)