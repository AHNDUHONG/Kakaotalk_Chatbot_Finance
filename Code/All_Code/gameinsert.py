import psycopg2

item = "'삼성전자'"
many = "5"
user = "'gdq153'"
# useruser = "gdq153"
money = "150000"

passwd = ''
db = psycopg2.connect(host='ec2-54-204-56-171.compute-1.amazonaws.com', dbname='d2p5j2up8o05rg',user='dywzgxybcyjnzu',password= passwd,port=5432)

cur=db.cursor()

cur.execute("SELECT * FROM game WHERE item = %s;"% (user))
rows = cur.fetchall()
# print(rows)

# if len(rows) != 0 :
cur.execute("UPDATE game SET money=%s WHERE userid=%s AND money IS NOT null;"% (money, user) )
    

# cur.execute("INSERT INTO game (userid, item, shares) VALUES (%s, %s, %s);"% (user, item, many) )

db.commit()

print("done!")
