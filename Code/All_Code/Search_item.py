from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
# # 로딩이 필요 할 때 time 라이브러리 사용 필요
import time

driver = webdriver.Chrome()
driver.get("https://www.ktb.co.kr/trading/popup/itemPop.jspx")

item_name = "삼성전자"

# # target_search : 종목명 검색
fir= ".input_txt"
target1= driver.find_element_by_css_selector(fir)
target1.send_keys(item_name)
target1.send_keys(Keys.RETURN)

sec= "td"
target2= driver.find_elements_by_css_selector(sec)[0].text
target3= driver.find_elements_by_css_selector(sec)[1].text

# # 확인 단계
print(target2)
print(target3)

import pandas_datareader.data as web


# # 국내 주식
# # naver finance에서 추출
item_code = target2
target_data = web.DataReader(item_code, 'naver')
last = (target_data.shape[0])
print(target_data.iloc[last - 1])

# # 종료 단계
# driver.close()
print("end...")