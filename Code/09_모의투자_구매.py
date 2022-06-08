# from flask import Flask, request
import requests
# import json
import pandas_datareader.data as web
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
# from datetime import datetime

# # 모의주식 구매
# @app.route('/api/buyitem', methods=['POST'])
# def buyitem():

passwd = 'b55d94be7d8dbef24e28a72a0dcb228fb48d1595665100e8da2cd1aafbe8bbbc'
db = psycopg2.connect(host='ec2-54-204-56-171.compute-1.amazonaws.com', dbname='d2p5j2up8o05rg',user='dywzgxybcyjnzu',password= passwd,port=5432)
cur=db.cursor()


# body = request.get_json() # 사용자가 입력한 데이터
target_item = '모의주식 카카오 5 구매'
# target_item = body['userRequest']['utterance']
ssstttrrr = target_item.split()

# user=유저, money=잔액, item=주식, many=매수한 주식 수
if len(ssstttrrr) >= 3 :
    item = "'%s'" % ssstttrrr[1]
    many = int(ssstttrrr[2])

else :
    item = "'%s'" % ("갤럭시")
    many = 1
    
user = "'human'"
# user = "'%s'" %str(body['userRequest']['user']['id'])
target_item = item

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

        # # 가격 추출 성공!
        item = "'%s'" % item_name
        cur.execute("SELECT * FROM game WHERE userid = %s;"% (user))
        rows = cur.fetchall()

        # # id가 없을 시 투자자금 1,000,000원 지급
        if len(rows) == 0 :
            cur.execute("INSERT INTO game (userid, money) VALUES (%s, %d);"% (user, 1000000) )

        # # 돈만 있는 쿼리
        cur.execute("SELECT * FROM game WHERE userid = %s AND money IS NOT null;"% (user))
        rows2 = cur.fetchall()

        # # 종목명과 id로 검색한 쿼리
        cur.execute("SELECT * FROM game WHERE userid=%s AND item = %s;"% (user, item))
        rows3 = cur.fetchall()

        # 잔액이 0이상이면 실행
        money = int(rows2[0][1]) - int(target_data) * many
        if money >= 0 : 

            # # 가지고 있는 주식 종목을 추가로 구매 
            if len(rows3) != 0 :
                shares = rows3[0][3] + many
                cur.execute("UPDATE game SET shares=%d WHERE userid=%s AND item = %s;"% (shares, user, item) )
                cur.execute("UPDATE game SET money=%d WHERE userid=%s AND money IS NOT null;"% (money, user) )
                result =  str(many) + "주를 구매했습니다."
                
            elif many <= 0:
                result = "수량을 확인해주세요."

            # # 가지고 있지 않은 주식을 구매
            else :
                cur.execute("INSERT INTO game (userid, item, shares) VALUES (%s, %s, %d);"% (user, item, many) )
                cur.execute("UPDATE game SET money=%d WHERE userid=%s AND money IS NOT null;"% (money, user) )
                result =  item_name + " " + str(many) + "주를 구매했습니다."
        else :
            result = "잔액이 부족합니다"

        db.commit()

    except:
        result = "해외 주식은 아직 구현을 못했습니다."

except AttributeError:
    result = "'" + target_item.strip() + "' 으로 검색결과가 없습니다.\n" + "찾는 주식이 있다면 주식명과 주가를 입력해주세요."