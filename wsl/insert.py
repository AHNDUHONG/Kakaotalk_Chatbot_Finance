# # 테이블 생성 + 데이터 집어넣기

import psycopg2


passwd = '5280c3caeed8c1cb512f19d6fc238a6ab642556e69c3050ddfe232c4c4372d0e'
db = psycopg2.connect(host='ec2-3-234-131-8.compute-1.amazonaws.com', dbname='d33p984cbdpnn',user='ndurbfpbebgdrc',password= passwd,port=5432)
cur=db.cursor()

# cur.execute("DROP TABLE test")

cur.execute("CREATE TABLE IF NOT EXISTS test (url varchar, title varchar);")

cur.execute("INSERT INTO test (url, title) VALUES (%s, %s);"
            , ("google.com", "구글입니다") )

db.commit()

print("good")
