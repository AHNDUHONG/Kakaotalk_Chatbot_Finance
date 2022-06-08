import psycopg2
from bs4 import BeautifulSoup
import requests
import pandas_datareader.data as web


passwd =                'b55d94be7d8dbef24e28a72a0dcb228fb48d1595665100e8da2cd1aafbe8bbbc'
db = psycopg2.connect(host='ec2-54-204-56-171.compute-1.amazonaws.com', dbname='d2p5j2up8o05rg',user='dywzgxybcyjnzu',password= passwd,port=5432)
cur=db.cursor()


item = "'카카오'"
many = "15"
user = "'gdq153'"
# useruser = "gdq153"
money = "'150000'"
target_item = "카카오 주가"

target_item = target_item.split(" ")
for i in range(len(target_item)):
    if (target_item[i] == '주가') or (target_item[i] == '주가n') or (target_item[i] == '주가\n'):
        del target_item[i]

y = target_item[0]
for i in range(1, len(target_item)):
    y = y + ' ' + target_item[i]

target_item = y


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://kr.investing.com/search/?q=' + target_item, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

try:
    item_code = soup.select_one('#fullColumn > div > div.js-section-wrapper.searchSection.allSection > div:nth-child(2) > div.js-inner-all-results-quotes-wrapper.newResultsContainer.quatesTable > a:nth-child(1) > span.second').text
    item_name = soup.select_one('#fullColumn > div > div.js-section-wrapper.searchSection.allSection > div:nth-child(2) > div.js-inner-all-results-quotes-wrapper.newResultsContainer.quatesTable > a:nth-child(1) > span.third').text

    try:
        # # 국내 주식
        # # naver finance에서 추출
        target_data = web.DataReader(item_code, 'naver')
        last = (target_data.shape[0])
        target_data = target_data.iloc[last - 1].loc["Close"]
        result = item_name+ " 가격은"+ target_data+ "원입니다"
        # print(result)

    except:
        # # 해외 주식
        # # yahoo finance에서 추출
        target_data = web.DataReader(item_code, 'yahoo')
        last = (target_data.shape[0])
        target_data = target_data.iloc[last - 1].loc["Close"]
        target_data = str(round(float(target_data), 2))
        result = item_name+ " 가격은 "+ target_data+ "$입니다"
        # print(result)

except AttributeError:
    result = "'" + target_item.strip() + "' 으로 검색결과가 없습니다.\n" + "찾는 주식이 있다면 주식명만을 입력해주세요."
    # print(result)

##########################################

# # 팔겠다 입력

cur.execute("SELECT * FROM game WHERE userid = %s AND item = %s;"% (user, item))
rows = cur.fetchall()

if len(rows) != 0:
    limit = rows[0][3] - int(many)

    cur.execute("SELECT * FROM game WHERE userid = %s AND money IS NOT null;"% (user))
    rows = cur.fetchall()

    if limit < 0 :
        result = "보유 주식보다 더 많이 팔 수 없습니다."
    elif limit == 0 :
        # # money 컬럼 update
        harmoney = (rows[0][1] + int(target_data) * int(many))
        cur.execute("UPDATE game SET money = %s WHERE userid = %s AND money IS NOT null;" % (harmoney, user))
        # # 해당 주식 행 삭제
        cur.execute("DELETE FROM game WHERE item = %s" % (item) )

        result =  str(many) + "주를 팔았습니다."
    elif limit < 0 :
        # # money 컬럼 update
        cur.execute("UPDATE game SET money WHERE userid = %s AND money IS NOT null;" % (rows[0][1] + int(target_data) * many))
        # # 해당 주식 수 update
        cur.execute("UPDATE game SET shares = %s WHERE userid = %s AND item = %s" % (limit, user, item)  )
        result = str(many) + "주를 팔았습니다."
    else :
        result = "알 수 없는 에러가 발생했습니다."


db.commit()
print(result)

print("done!")