import psycopg2

from datetime import datetime

# print(datetime.today().strftime('%Y-%m-%d'))


passwd =                'b55d94be7d8dbef24e28a72a0dcb228fb48d1595665100e8da2cd1aafbe8bbbc'
db = psycopg2.connect(host='ec2-54-204-56-171.compute-1.amazonaws.com', dbname='d2p5j2up8o05rg',user='dywzgxybcyjnzu',password= passwd,port=5432)
cur=db.cursor()

cur.execute("DROP TABLE score")

cur.execute("CREATE TABLE IF NOT EXISTS score (date varchar, id varchar, score varchar);")

# cur.execute("INSERT INTO score (date, id, score) VALUES (%s, %s, %s);"
#             , (datetime.today().strftime('%Y-%m-%d') , "woobin", 5) )

db.commit()

print("good")