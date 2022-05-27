import psycopg2
from datetime import datetime

passwd =                ''
db = psycopg2.connect(host='', dbname='',user='',password= passwd,port=5432)
cur=db.cursor()

# 날짜, id, 점수 
date_data = datetime.today().strftime('%Y-%m-%d')
id_data = "''"
idid_data = ''
score_data = '2'


# SELECT문 - id로 검색하여 조회
cur.execute("SELECT * FROM score WHERE id=%s;" % (id_data))
rows = cur.fetchall()
print(rows)
print(type(rows))


# rows 길이 = 0 
# 해당 id가 남긴 기록이 없음 = 첫 평가
# 점수를 포함한 데이터를 INSERT
if len(rows) == 0:
    cur.execute("INSERT INTO score (date, id, score) VALUES (%s, %s, %s);"
            , (datetime.today().strftime('%Y-%m-%d'), idid_data, score_data) )

# rows 길이 != 0
# 해당 id가 남긴 기록이 있음 = 최소 두 번째 평가
# 기존에 남긴 점수를 새로 UPDATE
else :
    cur.execute("UPDATE score SET date=%s, score=%s WHERE id=%s;"
            , (datetime.today().strftime('%Y-%m-%d'),score_data, idid_data) )




# cur.execute("SELECT * FROM score WHERE id=%s;" % (id_data))
# rows = cur.fetchall()
# print(rows)
# print(type(rows))

# POSTGRESQL DB에 COMMIT 하기
db.commit()



