import psycopg2


passwd =                'b55d94be7d8dbef24e28a72a0dcb228fb48d1595665100e8da2cd1aafbe8bbbc'
db = psycopg2.connect(host='ec2-54-204-56-171.compute-1.amazonaws.com', dbname='d2p5j2up8o05rg',user='dywzgxybcyjnzu',password= passwd,port=5432)
cur=db.cursor()

cur.execute("DROP TABLE test")

cur.execute("CREATE TABLE IF NOT EXISTS score (date varchar, id varchar, score smallint);")

# cur.execute("INSERT INTO score (url, title) VALUES (%s, %s);"
#             , ("naver.com", "네이버입니다") )

db.commit()

print("maked!")