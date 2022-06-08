import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate

url = "https://finance.naver.com/sise/sise_rise.naver"
response = requests.get(url)

html = response.text
soup = BeautifulSoup(html, 'html.parser')

# print("good")
title1 = soup.select('th')
col_list = []
# print(len(title1))

# 컬럼명 
for i in range(len(title1)):
    if (title1[i].text == "종목명") or (title1[i].text == "현재가") or (title1[i].text == "등락률"):
        col_list.append(title1[i].text)
print("col_list ", len(col_list))
print(col_list)

# title_list : 주식 종목 리스트
title2 = soup.find_all("a", class_="tltle")
title_list = []
print(len(title2)) # 1054개

for i in range(len(title2)):
    if len(title2[i].text) > 6:
        title_list.append(title2[i].text[0:7])
    else:
        title_list.append(title2[i].text)
    if len(title_list) == 10 :
        break
# print(title_list)
print("title_list ", len(title_list))

# # data_list : 종목별 데이터
title3 = soup.find_all("td", class_="number")
# print(len(title3)) # 10000개 데이터
data_list1 = []

for i in range(len(title3)):
    j = divmod(i ,10)
    if (j[1] == 0):
        data_list1.append(title3[i].text)
    if len(data_list1) == 10 :
        break
print(data_list1)

title4 = soup.find_all("span", class_="tah p11 red01")
print(len(title4)) # 1000개 데이터 
data_list2 = []
for i in range(len(title3)):
    data_list2.append(title4[i].text)
    if len(data_list2) == 10 :
        break
strip_list2 = []
for i in data_list2:
    i = i.strip()
    strip_list2.append(i)
print(strip_list2)

data_list = []
for i in range(len(data_list1)):
    data_list.append(data_list1[i])
    data_list.append(strip_list2[i])
print(data_list)
    
# title + data
step01_list = []
for i in range(len(title_list)):
    step01_list.append([])
    step01_list[i].append(title_list[i])
# print(step01_list)
    for j in range(len(data_list)):
        k = divmod(j, 2)
        if k[0] == i :
            step01_list[i].append(data_list[j])
print(step01_list)
print("step01 ", len(step01_list))

df = pd.DataFrame(step01_list, columns=['종목명', '현재가', '등락률'], index=range(1, 11))
df.to_string(justify="left")
# df = str(df)
print(df)