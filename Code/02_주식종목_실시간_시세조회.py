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