# # 테이블 생성 + 데이터 집어넣기

import psycopg2


passwd = ''
db = psycopg2.connect(host='', dbname='',user='',password= passwd,port=5432)
cur=db.cursor()

# cur.execute("DROP TABLE test")

cur.execute("CREATE TABLE IF NOT EXISTS test (url varchar, title varchar);")

cur.execute("INSERT INTO test (url, title) VALUES (%s, %s);"
            , ("google.com", "구글입니다") )

db.commit()

print("good")
