import psycopg2
import pandas as pd
import requests
# user1 = "'gdq153'"
body = request.get_json() # 사용자가 입력한 데이터
user1 = "'%s'" %str(body['userRequest']['user']['id'])

passwd = 'b55d94be7d8dbef24e28a72a0dcb228fb48d1595665100e8da2cd1aafbe8bbbc'
db = psycopg2.connect(host='ec2-54-204-56-171.compute-1.amazonaws.com', dbname='d2p5j2up8o05rg',user='dywzgxybcyjnzu',password= passwd,port=5432)

cur=db.cursor()



cur.execute("SELECT * FROM game WHERE userid=%s AND money IS null;"% (user1)) 
rows = cur.fetchall()
print(rows)
# print(len(rows))
stock_list = []
for i in range(len(rows)):
    stock_list.append(rows[i][2])
print(stock_list)

many_list = []
for i in range(len(rows)):
    many_list.append(rows[i][3])
print(many_list)

final_list = []
for i in range(len(stock_list)):
    final_list.append([])
    final_list[i].append(stock_list[i])
    for j in range(len(many_list)):
        if i == j:

            final_list[i].append(many_list[i])
# print(final_list)

df = pd.DataFrame(final_list, columns=["종목명", "주식수"], index=range(1, len(stock_list)+1))
print(df)





# cur.execute("SELECT money FROM game WHERE userid=%s AND money IS NOT null;"% (user1)) 
# rows = cur.fetchone()
# str(rows)
# print(rows)
#     # cur.execute("INSERT INTO game (userid, item, shares) VALUES (%s, %s, %s);"% (user, item, many) )

# db.commit()


# rows = cur.fetchall()
# print(rows)