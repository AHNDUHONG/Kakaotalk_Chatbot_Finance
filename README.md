# 카카오톡 휴먼주식도우미챗봇 프로젝트

![image](https://user-images.githubusercontent.com/101306629/171777658-641f5831-608c-4b8f-9b59-0c895c592d07.png)

* 본 프로젝트는 휴먼교육센터학원 주도하에 이루어진 프로젝트입니다
* 일정: 2022.05.20 ~ 2022.06.03
* 프로젝트 참여 인원은 총 4명이며 팀장: 안두홍, 팀원: 조해성, 황우빈, 김민균으로 이루어져 있습니다.
* IT 교육을 받은 이래로 첫 프로젝트이기 때문에 개인의 역량과 시간 관리 부분에서 많은 어려움이 있었으나 성공적으로 마쳤습니다.
* 카카오톡 오픈 빌더를 활용하여 DB연동, Heroku 서버 연동, 웹 크롤링, 판다스, 카카오톡 기본 소스에 대해 더 자세히 알게 된 좋은 겸험이었던 것 같습니다.

## 개요
* 주식 입문자를 위한 카카오톡 챗봇을 개발하는 프로젝트 기획 및 과정, 결과 단계를 나타내고 있습니다.

## 목차
1. 프로젝트 분석 개요
2. 프로젝트 

### 1. 프로젝트 분석 개요
#### 1-1. 데이터 수집
        - 웹 크롤링
        - Pandas 활용 데이터 가공 및 추출
        - 데이터 웹 서치
#### 1-2. 챗봇 서비스 기획
        - 시나리오 구성
        - 블록 구성
        - 카카오톡 스킬 및 Document 확인
#### 1-3. 챗봇 서비스 구현
        - 시나리오 작성
        - 블록 작성
#### 1-4 카카오톡 스킬 구현
        - 크롤링 및 데이터 Heroku 서버 적용 및 배포
        - DB 구축 및 연동(PostSQL사용)
        - 카카오톡 엔티티 작성

### 2. 카카오톡 챗봇 시스템 Flow Chart
![image](https://user-images.githubusercontent.com/101306629/171781823-b6eb8e9c-0f34-49fe-8fcc-8be837eb049c.png)

### 3. 시나리오 구성 개요
![image](https://user-images.githubusercontent.com/101306629/171781871-fa5043e9-4235-42f1-9a7d-14e95ab1d2e7.png)

### 4. 개발 환경
![image](https://user-images.githubusercontent.com/101306629/171782229-2208d04c-c990-4829-9958-bfff6c37194e.png)

### 5. 프로젝트 수행 기록
#### 5-1. 주식 시세 실시간 응답
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
