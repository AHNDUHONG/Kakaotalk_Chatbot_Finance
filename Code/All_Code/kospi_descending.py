import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://finance.naver.com/sise/sise_fall.naver?sosok=0"
response = requests.get(url)

html = response.text
soup = BeautifulSoup(html, 'html.parser')
# # col_list : 종목명  현재가 등락률
title1 = soup.select('th')
col_list = []
for i in range(len(title1)):
    if (title1[i].text == "종목명") or (title1[i].text == "현재가") or (title1[i].text == "등락률"):
        col_list.append(title1[i].text)
# print("col_list ", len(col_list))
# print(col_list)

# # title_list : 주식 종목 리스트
title2 = soup.findAll("a", class_="tltle")
title_list = []
for i in range(len(title2)):
    if len(title2[i].text) > 6:
        title_list.append(title2[i].text[0:6]+"...")
    else:
        title_list.append(title2[i].text)
    if len(title_list) == 10 :
        break
# print(title_list)
# print("title_list " , len(title_list))

# # data_list : 종목별 데이터
title3 = soup.find_all("td", class_="number")
data_list = []
for i in range(len(title3)):
    j = divmod(i, 10)
    if (j[1] == 0) or (j[1] == 2):
        data_list.append(title3[i].text.strip())
    if len(data_list) == 40 :
        break
# print(data_list)
# print("data_list ", len(data_list))
# # title + data
step01_list = []
for i in range(len(title_list)):
    step01_list.append([])
    step01_list[i].append(title_list[i])
    for j in range(len(data_list)):
        k = divmod(j, 2)
        if k[0] == i :
            step01_list[i].append(data_list[j])
# print("step01 ", len(step01_list))
# print(step01_list)
result = str(pd.DataFrame(step01_list, columns=col_list, index=range(1, 11)))
print(result)


