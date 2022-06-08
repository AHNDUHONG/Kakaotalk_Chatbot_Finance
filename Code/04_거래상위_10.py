import requests
from bs4 import BeautifulSoup
import pandas as pd

# # 거래상위 100개 페이지
url = "https://finance.naver.com/sise/sise_quant.naver"
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
# print("goo")

# # col_list : 종목명 현재가 거래량
title1 = soup.select('th')    
col_list = []
# print(len(title1)) # 12개

# 컬럼명
for i in range(len(title1)):
    if (title1[i].text == "종목명") or (title1[i].text == "현재가") or (title1[i].text == "거래량"):
        col_list.append(title1[i].text)
# print("col_list ", len(col_list))
# print(col_list)

# title_list : 주식 종목 리스트
title2 = soup.findAll("a", class_="tltle")
title_list = []
# print(len(title2)) # 100개
for i in range(len(title2)):
    if len(title2[i].text) > 7:
        title_list.append(title2[i].text[0:7]+"...")
    else:
        title_list.append(title2[i].text)
    if len(title_list) == 10 :
        break
print(title_list)
# print("title_list ", len(title_list)) # 10개

# data_list : 현재가 , 거래량
title3 = soup.find_all("td", class_="number")
# print(len(title3)) # 1000개
data_list = []

for i in range(len(title3)):
    j = divmod(i, 10)
    if (j[1] == 0) or (j[1] == 3):
        data_list.append(title3[i].text)
        if len(data_list) == 20 :
            break
# print(data_list)

# title + data
step01_list = []
for i in range(len(title_list)):
    step01_list.append([])
    step01_list[i].append(title_list[i])
# print(step01_list) # 10개
    for j in range(len(data_list)):
        k = divmod(j, 2)
        if k[0] == i :
            step01_list[i].append(data_list[j])
print(step01_list)

df = pd.DataFrame(step01_list, columns=['종목명', '현재가', '거래량'], index=range(1, 11))
df = str(df)
print(df)



# #     # # # topactive_list : 최종 리스트
# #     # topactive_list = []
# #     # for i in range(len(col_list)):
# #     #     topactive_list.append(col_list[i])
# #     # for i in range(len(step01_list)):
# #     #     topactive_list.append(step01_list[i])
# #     # print("topactive_list ", len(topactive_list))
# #     # print(topactive_list)

# # else:
# #     print(response.status_code)

# # # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html

# # df2 = pd.DataFrame(step01_list)
# # print(df2)

# # #contentarea > div.box_type_l > table > tbody

# title_list.insert(1,data_list[:4])
# # print(title_list)
# print(set(title_list))