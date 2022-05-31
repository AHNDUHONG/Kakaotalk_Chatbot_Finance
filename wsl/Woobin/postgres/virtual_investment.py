import psycopg2

passwd = 'b55d94be7d8dbef24e28a72a0dcb228fb48d1595665100e8da2cd1aafbe8bbbc'
db = psycopg2.connect(host='ec2-54-204-56-171.compute-1.amazonaws.com', dbname='d2p5j2up8o05rg',user='dywzgxybcyjnzu',password= passwd,port=5432)

cur=db.cursor()

cur.execute("DROP TABLE game")

cur.execute("CREATE TABLE IF NOT EXISTS game (userid varchar, money integer, item varchar, shares integer);")

cur.execute("INSERT INTO game (userid, money) VALUES (%s, %s);"
            , ("gdq153", "1000000") )

db.commit()

print("done!")