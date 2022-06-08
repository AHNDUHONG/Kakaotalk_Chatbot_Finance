import psycopg2
from datetime import datetime

passwd =                ''
db = psycopg2.connect(host='ec2-54-204-56-171.compute-1.amazonaws.com', dbname='d2p5j2up8o05rg',user='dywzgxybcyjnzu',password= passwd,port=5432)
cur=db.cursor()
date_data = "'%s'" %(datetime.today().strftime('%Y-%m-%d'))
datedate_data = '%s' %(datetime.today().strftime('%Y-%m-%d'))


cur.execute("SELECT * FROM score WHERE date = %s;" % (date_data))
rows = cur.fetchall()

print(rows)
# print(type(rows))
# print((rows[0][0]))
# print(type(rows[0][0]))
