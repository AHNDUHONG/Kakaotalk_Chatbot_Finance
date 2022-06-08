import psycopg2
import requests

# user1 = gdq1
body = request.get_json() # 사용자가 입력한 데이터
user1 = "'%s'" %str(body['userRequest']['user']['id']) 

passwd = 'b55d94be7d8dbef24e28a72a0dcb228fb48d1595665100e8da2cd1aafbe8bbbc'
db = psycopg2.connect(host='ec2-54-204-56-171.compute-1.amazonaws.com', dbname='d2p5j2up8o05rg',user='dywzgxybcyjnzu',password= passwd,port=5432)

cur=db.cursor()

cur.execute("SELECT * FROM game WHERE userid=%s AND money IS NOT null;"% (user1)) 
rows = cur.fetchall()

# print(rows)
target = rows[0][1]
# print(target)
target = str(target)
print(target)