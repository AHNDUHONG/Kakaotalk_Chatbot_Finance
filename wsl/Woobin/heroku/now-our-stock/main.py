from tokenize import String
from flask import Flask, request
import requests
# import json
import pandas_datareader.data as web
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
from datetime import datetime

app = Flask(__name__)

passwd = ''
db = psycopg2.connect(host='ec2-54-204-56-171.compute-1.amazonaws.com', dbname='d2p5j2up8o05rg',user='dywzgxybcyjnzu',password= passwd,port=5432)
cur=db.cursor()

@app.route('/')
def hello_world():
    return 'bye, user!'

# 카카오톡 텍스트형 응답
@app.route('/api/sayHello', methods=['POST'])
def sayHello():
    body = request.get_json() # 사용자가 입력한 데이터
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "안녕 hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody


# 카카오톡 이미지형 응답
@app.route('/api/showHello', methods=['POST'])
def showHello():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleImage": {
                        "imageUrl": "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
                        "altText": "hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody


# # 주식명으로 주가 응답
@app.route('/api/itemdata', methods=['POST'])
def itemdata():
    body = request.get_json() # 사용자가 입력한 데이터

    target_item = body['userRequest']['utterance']

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
    

    responseData = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseData


# 유저가 입력 한 값 반환
@app.route('/api/test', methods=['POST'])
def test():
    # print("ddd")
    body = request.get_json() # 사용자가 입력한 데이터
    # msg = "셀레니움"
    # name = body['userRequest']
    # age = type(body['userRequest']['utterance'])
    body2 = str(body['userRequest']['utterance']).strip()
    body3 = str(body['userRequest']['user']['id'])
    print(body)
    age = "27"
    responseData = {
        "version": "2.0",
        "data": {
                "landingUrl": body2
                , "msg" : body
                , "name" : body3
                , "age" : "age"
        }
    }

    return responseData


# # 거래상위 크롤링 응답
@app.route('/api/activetop', methods=['POST'])
def activetop():
    # body = request.get_json() # 사용자가 입력한 데이터

    # # 거래상위 100개 페이지
    url = "https://finance.naver.com/sise/sise_quant.naver"
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # # col_list : 종목명 현재가 시가총액
        title1 = soup.select('th')    
        col_list = []
        for i in range(len(title1)):
            # if (title1[i].text == "종목명") or (title1[i].text == "현재가") or (title1[i].text == "거래량") or (title1[i].text == "거래대금") or (title1[i].text == "시가총액"):
            if (title1[i].text == "종목명") or (title1[i].text == "현재가") or (title1[i].text == "시가총액"):
                col_list.append(title1[i].text)
        print("col_list ", len(col_list))
        print(col_list)

        # # title_list : 주식 종목 리스트
        title2 = soup.findAll("a", class_="tltle")
        title_list = []
        for i in range(len(title2)):
            # title2[i] 
            title_list.append(title2[i].text)
            if len(title_list) == 10 :
                break
        # print(title_list)
        print("title_list " , len(title_list))

        # # data_list : 종목별 데이터
        title3 = soup.find_all("td", class_="number")
        data_list = []
        for i in range(len(title3)):
            j = divmod(i, 10)
            if (j[1] == 0)or (j[1] == 7):
                data_list.append(title3[i].text)
            if len(data_list) == 40 :
                break

        # print(data_list)
        print("data_list ", len(data_list))

        # # title + data
        step01_list = []
        for i in range(len(title_list)):
            step01_list.append([])
            step01_list[i].append(title_list[i])
            for j in range(len(data_list)):
                k = divmod(j, 2)
                if k[0] == i :
                    step01_list[i].append(data_list[j])
        print("step01 ", len(step01_list))
        print(step01_list)

        result = str(pd.DataFrame(step01_list, columns=col_list, index=range(1, 11)))
        print(result)

    else:
        print(response.status_code)
    

    responseData = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseData


# # 검색상위 크롤링 응답
@app.route('/api/searchtop', methods=['POST'])
def searchtop():

    # # 거래상위 100개 페이지
    url = "https://finance.naver.com/sise/lastsearch2.naver"
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        print("good")

        # # col_list : 종목명 검색비율 현재가 
        title1 = soup.select('th')    
        col_list = []
        for i in range(len(title1)):
            if (title1[i].text == "종목명") or (title1[i].text == "검색비율") or (title1[i].text == "현재가"):
                col_list.append(title1[i].text)
        print("col_list ", len(col_list))
        print(col_list)

        # # title_list : 주식 종목 리스트
        title2 = soup.findAll("a", class_="tltle")
        title_list = []
        for i in range(len(title2)):
            title_list.append(title2[i].text)

            if i == 9 :
                break
        # print(title_list)
        print("title_list " , len(title_list))

        # # data_list : 종목별 데이터
        title3 = soup.find_all("td", class_="number")
        data_list = []
        for i in range(len(title3)):
            j = divmod(i, 10)
            if (j[1] == 0) or (j[1] == 1):
                data_list.append(title3[i].text)
            if len(data_list) == 40 :
                break
        # print(data_list)
        print("data_list ", len(data_list))


        # # title + data
        step01_list = []
        for i in range(len(title_list)):
            step01_list.append([])
            step01_list[i].append(title_list[i])
            for j in range(len(data_list)):
                k = divmod(j, 2)
                if k[0] == i :
                    step01_list[i].append(data_list[j])
        print("step01 ", len(step01_list))
        print(step01_list)

        result = str(pd.DataFrame(step01_list, columns=col_list, index=range(1, 11)))
        print(result)

    else:
        print(response.status_code)

    responseData = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseData

# # db에 점수추가
@app.route('/api/dbinsert', methods=['POST'])
def dbinsert():
    body = request.get_json() # 사용자가 입력한 데이터

    # date_data = datetime.today().strftime('%Y-%m-%d')
    id_data = "'%s'" %str(body['userRequest']['user']['id'])
    idid_data = '%s' %str(body['userRequest']['user']['id'])
    score_data = str(list(body['userRequest']['utterance'])[1])
    cur=db.cursor()

    cur.execute("SELECT * FROM score WHERE id=%s;" % (id_data))
    rows = cur.fetchall()
    
    if len(rows) == 0:
        cur.execute("INSERT INTO score (date, id, score) VALUES (%s, %s, %s);"
                , (datetime.today().strftime('%Y-%m-%d'), idid_data, score_data) )

    else :
        cur.execute("UPDATE score SET date=%s, score=%s WHERE id=%s;"
                , (datetime.today().strftime('%Y-%m-%d'),score_data, idid_data) )


    db.commit()

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "점수가 반영되었습니다.\n감사합니다."
                    }
                }
            ]
        }
    }

    return responseBody


# # # 주식 팔기
# @app.route('/api/sellitem', methods=['POST'])
# def sellitem():
#     body = request.get_json() # 사용자가 입력한 데이터

#     user = "'%s'" %str(body['userRequest']['user']['id'])
#     user = '%s' %str(body['userRequest']['user']['id'])
#     item = str(list(body['userRequest']['utterance'])[1])
#     many = str(list(body['userRequest']['utterance'])[1])
#     target_item = str(list(body['userRequest']['utterance'])[1])

#     target_item = target_item.split(" ")
#     for i in range(len(target_item)):
#         if (target_item[i] == '주가') or (target_item[i] == '주가n') or (target_item[i] == '주가\n'):
#             del target_item[i]

#     y = target_item[0]
#     for i in range(1, len(target_item)):
#         y = y + ' ' + target_item[i]

#     target_item = y


#     headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#     data = requests.get('https://kr.investing.com/search/?q=' + target_item, headers=headers)
#     soup = BeautifulSoup(data.text, 'html.parser')

#     try:
#         item_code = soup.select_one('#fullColumn > div > div.js-section-wrapper.searchSection.allSection > div:nth-child(2) > div.js-inner-all-results-quotes-wrapper.newResultsContainer.quatesTable > a:nth-child(1) > span.second').text
#         item_name = soup.select_one('#fullColumn > div > div.js-section-wrapper.searchSection.allSection > div:nth-child(2) > div.js-inner-all-results-quotes-wrapper.newResultsContainer.quatesTable > a:nth-child(1) > span.third').text

#         try:
#             # # 국내 주식
#             # # naver finance에서 추출
#             target_data = web.DataReader(item_code, 'naver')
#             last = (target_data.shape[0])
#             target_data = target_data.iloc[last - 1].loc["Close"]
#             result = item_name+ " 가격은"+ target_data+ "원입니다"

#         except:
#             # # 해외 주식
#             # # yahoo finance에서 추출
#             target_data = web.DataReader(item_code, 'yahoo')
#             last = (target_data.shape[0])
#             target_data = target_data.iloc[last - 1].loc["Close"]
#             target_data = str(round(float(target_data), 2))
#             # result = item_name+ " 가격은 "+ target_data+ "$입니다"

#     except AttributeError:
#         result = "'" + target_item.strip() + "' 으로 검색결과가 없습니다.\n" + "찾는 주식이 있다면 주식명만을 입력해주세요."

#     cur.execute("SELECT * FROM game WHERE userid = %s AND item = %s;"% (user, item))
#     rows = cur.fetchall()

#     if len(rows) != 0:
#         limit = rows[0][3] - int(many)

#         cur.execute("SELECT * FROM game WHERE userid = %s AND money IS NOT null;"% (user))
#         rows = cur.fetchall()

#         if limit < 0 :
#             result = "보유 주식보다 더 많이 팔 수 없습니다."
#         elif limit == 0 :
#             # # money 컬럼 update
#             harmoney = (rows[0][1] + int(target_data) * int(many))
#             cur.execute("UPDATE game SET money = %s WHERE userid = %s AND money IS NOT null;" % (harmoney, user))
#             # # 해당 주식 행 삭제
#             cur.execute("DELETE FROM game WHERE item = %s" % (item) )

#             result =  str(many) + "주를 팔았습니다."
#         elif limit < 0 :
#             # # money 컬럼 update
#             cur.execute("UPDATE game SET money WHERE userid = %s AND money IS NOT null;" % (rows[0][1] + int(target_data) * many))
#             # # 해당 주식 수 update
#             cur.execute("UPDATE game SET shares = %s WHERE userid = %s AND item = %s" % (limit, user, item)  )
#             result = str(many) + "주를 팔았습니다."
#         else :
#             result = "알 수 없는 에러가 발생했습니다."

#     db.commit()

#     responseBody = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "simpleText": {
#                             "text": result
#                         }
#                     }
#                 ]
#             }
#         }

#     return responseBody



# # # 모의주식 구매
# @app.route('/api/buyitem', methods=['POST'])
# def buyitem():

#     body = request.get_json() # 사용자가 입력한 데이터
#     target_item = body['userRequest']['utterance']
#     # target_item = '모의주식 삼성전자 10 구매'

#     ssstttrrr = target_item.split()

#     item = "'%s'" % ssstttrrr[1]
#     many = int(ssstttrrr[2])
#     user = "'%s'" %str(body['userRequest']['user']['id'])
#     useruser = '%s' %str(body['userRequest']['user']['id'])


#     # user=유저, money=잔액, item=주식, many=매수한 주식 수

#     target_item = ssstttrrr[1]


#     headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#     data = requests.get('https://kr.investing.com/search/?q=' + target_item, headers=headers)
#     soup = BeautifulSoup(data.text, 'html.parser')

#     try:
#         item_code = soup.select_one('#fullColumn > div > div.js-section-wrapper.searchSection.allSection > div:nth-child(2) > div.js-inner-all-results-quotes-wrapper.newResultsContainer.quatesTable > a:nth-child(1) > span.second').text
#         item_name = soup.select_one('#fullColumn > div > div.js-section-wrapper.searchSection.allSection > div:nth-child(2) > div.js-inner-all-results-quotes-wrapper.newResultsContainer.quatesTable > a:nth-child(1) > span.third').text

#         try:
#             # # 국내 주식
#             # # naver finance에서 추출
#             target_data = web.DataReader(item_code, 'naver')
#             last = (target_data.shape[0])
#             target_data = target_data.iloc[last - 1].loc["Close"]
#             result = item_name+ " 가격은"+ target_data+ "원입니다"
#             # print(result)

#         except:
#             # # 해외 주식
#             # # yahoo finance에서 추출
#             target_data = web.DataReader(item_code, 'yahoo')
#             last = (target_data.shape[0])
#             target_data = target_data.iloc[last - 1].loc["Close"]
#             target_data = str(round(float(target_data), 2))
#             result = item_name+ " 가격은 "+ target_data+ "$입니다"
#             # print(result)

#     except AttributeError:
#         result = "'" + target_item.strip() + "' 으로 검색결과가 없습니다.\n" + "찾는 주식이 있다면 주식명만을 입력해주세요."
#         # print(result)

#     #

#     # cur.execute("SELECT * FROM game WHERE userid = %s;"% (user))
#     # rows = cur.fetchall()
#     # print(rows)


#     # # id가 없을 시 투자자금 1,000,000원 지급
#     # if len(rows) == 0 :
#     #     cur.execute("INSERT INTO game (userid, money) VALUES (%s, %d);"% (user, 1000000) )
#     #     # cur.execute("INSERT INTO game (userid, item, shares) VALUES (%s, %s, %d);"% (user, item, many) )

    
#     # cur.execute("SELECT * FROM game WHERE userid = %s;"% (user))
#     # rows = cur.fetchall()

#     # cur.execute("SELECT * FROM game WHERE userid = %s AND item IS null;"% (user))
#     # rows2 = cur.fetchall()
#     # print(rows2[0][1])

#     # # 잔액이 0이상이면 실행
#     # money = rows2[0][1] - int(target_data) * many
#     # if money >= 0 : 
#     #     # 존재하는 id
#     #     if len(rows) != 0 :
            
#     #         cur.execute("SELECT * FROM game WHERE userid=%s AND item = %s;"% (user, item))
#     #         rows = cur.fetchall()

#     #         # 가지고 있는 주식 종목을 추가로 구매 
#     #         if len(rows) != 0 :
#     #             shares = rows[0][3] + many
#     #             # cur.execute("UPDATE game SET shares=%d WHERE userid=%s AND shares IS NOT null;"% (shares, user) )
#     #             cur.execute("UPDATE game SET shares=%d WHERE userid=%s AND item = %s;"% (shares, user, item) )
#     #             cur.execute("UPDATE game SET money=%d WHERE userid=%s AND money IS NOT null;"% (money, user) )
#     #             result = "구매가 완료되었습니다."
                
#     #         # 가지고 있지 않은 주식을 구매
#     #         else :
#     #             cur.execute("INSERT INTO game (userid, item, shares) VALUES (%s, %s, %d);"% (user, item, many) )
#     #             cur.execute("UPDATE game SET money=%d WHERE userid=%s AND money IS NOT null;"% (money, user) )
#     #             result = "구매가 완료되었습니다."

#     # else :
#     #     result = "잔액이 부족합니다."

#     # db.commit()

# ########################################

#     cur.execute("SELECT * FROM game WHERE userid = %s;"% (user))
#     rows = cur.fetchall()
#     print(rows)



#     # id가 없을 시 투자자금 1,000,000원 지급
#     if len(rows) == 0 :
#         cur.execute("INSERT INTO game (userid, money) VALUES (%s, %d);"% (user, 1000000) )
#         # cur.execute("INSERT INTO game (userid, item, shares) VALUES (%s, %s, %d);"% (user, item, many) )


#     cur.execute("SELECT * FROM game WHERE userid = %s;"% (user))
#     rows = cur.fetchall()

#     cur.execute("SELECT * FROM game WHERE userid = %s AND item IS null;"% (user))
#     rows2 = cur.fetchall()



#     # 잔액이 0이상이면 실행
#     money = rows2[0][1] - int(target_data) * many
#     if money >= 0 : 
#         # 존재하는 id
#         if len(rows) != 0 :
            
#             cur.execute("SELECT * FROM game WHERE userid=%s AND item = %s;"% (user, item))
#             rows = cur.fetchall()

#             # 가지고 있는 주식 종목을 추가로 구매 
#             if len(rows) != 0 :
#                 shares = rows[0][3] + many
#                 # cur.execute("UPDATE game SET shares=%d WHERE userid=%s AND shares IS NOT null;"% (shares, user) )
#                 cur.execute("UPDATE game SET shares=%d WHERE userid=%s AND item = %s;"% (shares, user, item) )
#                 cur.execute("UPDATE game SET money=%d WHERE userid=%s AND money IS NOT null;"% (money, user) )
#                 result = "구매 완료"
                
#             # 가지고 있지 않은 주식을 구매
#             else :
#                 cur.execute("INSERT INTO game (userid, item, shares) VALUES (%s, %s, %d);"% (user, item, many) )
#                 cur.execute("UPDATE game SET money=%d WHERE userid=%s AND money IS NOT null;"% (money, user) )
#                 result = "구매 완료"
#     else :
#         result = "잔액이 부족합니다"


#     cur.execute("SELECT * FROM game WHERE userid = %s;"% (user))
#     rows = cur.fetchall()
#     print(rows)


#     db.commit()



# ##########################333

#     responseBody = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "simpleText": {
#                             # "text": "result"
#                             "text": result
#                         }
#                     }
#                 ]
#             }
#         }

#     return responseBody
