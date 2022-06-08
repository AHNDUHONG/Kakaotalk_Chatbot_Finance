# 카카오톡 휴먼주식도우미챗봇 프로젝트

![image](https://user-images.githubusercontent.com/101306629/171777658-641f5831-608c-4b8f-9b59-0c895c592d07.png)

* 본 프로젝트는 휴먼교육센터학원 주도하에 이루어진 프로젝트입니다
* 일정: 2022.05.20 ~ 2022.06.03
* IT 교육을 받은 이래로 첫 프로젝트이기 때문에 개인의 역량과 시간 관리 부분에서 많은 어려움이 있었으나 성공적으로 마쳤습니다.
* 카카오톡 오픈 빌더를 활용하여 DB연동, Heroku 서버 연동, 웹 크롤링, 판다스, 카카오톡 기본 소스에 대해 더 자세히 알게 된 좋은 겸험이었던 것 같습니다.

## 개요
* 주식 입문자를 위한 카카오톡 챗봇을 개발하는 프로젝트 기획 및 과정, 결과 단계를 나타내고 있습니다.

## 참여 인원
* **팀장: 안두홍 [Github](https://github.com/AHNDUHONG)**
* **팀원: 조해성 [Github](https://github.com/Griotold)**
* **팀원: 황우빈 [Github](https://github.com/WoobinHwang)**
* **팀원: 김민균 [Github](https://github.com/kmk3593)**

## 목차
1. 프로젝트 분석 개요
2. 카카오톡 챗봇 시스템 Flow Chart
3. 시나리오 구성 개요
4. 개발 환경
5. 프로젝트 수행기록 

## 1. 프로젝트 분석 개요
### 1-1. 데이터 수집
        - 웹 크롤링
        - Pandas 활용 데이터 가공 및 추출
        - 데이터 웹 서치
### 1-2. 챗봇 서비스 기획
        - 시나리오 구성
        - 블록 구성
        - 카카오톡 스킬 및 Document 확인
### 1-3. 챗봇 서비스 구현
        - 시나리오 작성
        - 블록 작성
### 1-4 카카오톡 스킬 구현
        - 크롤링 및 데이터 Heroku 서버 적용 및 배포
        - DB 구축 및 연동(PostSQL사용)
        - 카카오톡 엔티티 작성

## 2. 카카오톡 챗봇 시스템 Flow Chart
![image](https://user-images.githubusercontent.com/101306629/171781823-b6eb8e9c-0f34-49fe-8fcc-8be837eb049c.png)

## 3. 시나리오 구성 개요
![image](https://user-images.githubusercontent.com/101306629/171781871-fa5043e9-4235-42f1-9a7d-14e95ab1d2e7.png)

## 4. 개발 환경
![image](https://user-images.githubusercontent.com/101306629/171782229-2208d04c-c990-4829-9958-bfff6c37194e.png)

## 5. 프로젝트 수행 기록
### 5-1. 주식 시세 실시간 응답
#### 기획
* 사용자가 원하는 주식명을 입력하면 현재 가격을 응답하는 기능
* Pandas를 이용하여 주식 시세를 불러오고 웹 크롤링으로 Pandas에 쓸 주식 코드를 크롤링

#### 실제 챗봇 반영 결과
![image](https://user-images.githubusercontent.com/101306629/172610891-23e2661a-db89-4d2e-b1f2-63a64b7f1a5d.png)

#### 사용 코드
```python
import requests
from bs4 import BeautifulSoup
import pandas_datareader.data as web

target_item = "삼성전자"


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
        result = item_name+ "가격은"+ target_data+ "원입니다"
        print(result)

    except:
        # # 해외 주식
        # # yahoo finance에서 추출
        target_data = web.DataReader(item_code, 'yahoo')
        last = (target_data.shape[0])
        target_data = target_data.iloc[last - 1].loc["Close"]
        target_data = str(round(float(target_data), 2))
        result = item_name+ "가격은 "+ target_data+ "달러입니다"
        print(result)
        # print("yes")

except AttributeError:
    result = "'" + target_item + "' 으로 검색했을때 나오는 데이터가 없습니다."
    print(result)

print("good")
```

### 5-2. 모의투자 (DB활용)
#### 기획
* 체험용으로 투자를 체험 가능한 기능을 구현
* DB에 사용자의 고유ID, 가상자산, 보유주식 등 정보를 저장하며 상황에 맞게 사칙연산도 가능하여 사용자에게 전달함

#### 알고리즘
![image](https://user-images.githubusercontent.com/101306629/172611332-84321457-b832-4016-8b31-46a618e12098.png)

#### 실제 챗봇 반영 결과
![image](https://user-images.githubusercontent.com/101306629/172611931-d7ee9812-0504-4dc0-85b9-7aa099c914e9.png)

#### 사용 코드 (일부)
``` python
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
```
