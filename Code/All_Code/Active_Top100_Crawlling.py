from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
# # 로딩이 필요 할 때 time 라이브러리 사용 필요
import time

driver = webdriver.Chrome()
driver.get("https://finance.naver.com/sise/sise_quant.naver")

# # target_col : 컬럼명
# 종목명 검색비율 현재가 전일비 등락률 거래량 시가 고가 저가 PER ROE
thi = "th"
target_col= driver.find_elements_by_css_selector(thi)

# # target1 : 종목명
fir= ".tltle"
target1= driver.find_elements_by_css_selector(fir)

# # target2 : 종목 별 수치(10개씩)
sec= ".number"
target2= driver.find_elements_by_css_selector(sec)

# # target2에 상승 하락을 추가하여 수정 divmod()이용
for i in range(len(target2)):

    target2[i] = target2[i].text

for i in range(len(target2)):

    if (divmod(i, 10)[1] == 2):
        if float(target2[i].split("%")[0]) > 0 :
            target2[i-1] = "상승 " + target2[i-1]
        elif float(target2[i].split("%")[0]) < 0 :
            target2[i-1] = "하락 " + target2[i-1]
        else :
            continue

# # col_list 만들기
col_list = []
for i in target_col:
    if i.text != "순위":
        col_list.append(i.text)

# # target2와 target1을 합치기
target_list= []

for i in range(len(target1)):
    target_list.append([])
    target_list[i].append(target1[i].text)

    for j in range(len(target2)):
        if divmod(j, 10)[0] == i:
            target_list[i].append(target2[j])

# # col_list와 target_ist 합치기
active_top100_list = []
active_top100_list.append(col_list)
for i in range(len(target_list)):

    active_top100_list.append(target_list[i])

# # 확인 단계
print(active_top100_list)
print(len(active_top100_list))
# print(len(target1))
# print(len(target2))

# # 종료 단계
driver.close()
print("end...")