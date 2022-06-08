import requests
from bs4 import BeautifulSoup
import pandas as pd

# # 거래상위 100개 페이지
url = "https://finance.naver.com/sise/lastsearch2.naver"
response = requests.get(url)
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # print("good")

    # # col_list : 현재가 전일비 등락률 거래량 거래대금 매수호가 매도호가 시가총액 PER ROE
    title1 = soup.select('th')    
    col_list = []
    for i in range(len(title1)):
        if (title1[i].text == "종목명") or (title1[i].text == "검색비율") or (title1[i].text == "현재가") or (title1[i].text == "거래량") or (title1[i].text == "시가"):
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
    # print("title_list " , title_list)

    # # data_list : 종목별 데이터
    title3 = soup.find_all("td", class_="number")
    data_list = []
    for i in range(len(title3)):
        j = divmod(i, 10)
        if (j[1] == 0) or (j[1] == 1) or (j[1] == 4) or (j[1] == 5):
            data_list.append(title3[i].text)
        if len(data_list) == 40 :
            break
    # print(data_list)
    # print("data_list ", data_list)


#     # # title + data
#     step01_list = []
#     for i in range(len(title_list)):
#         step01_list.append(title_list[i])
#         for j in range(len(data_list)):
#             k = divmod(j, 4)
#             if k[0] == i :
#                 step01_list.append(data_list[j])
#     print("step01 ", step01_list)
#     # print(step01_list)


#     # # # topactive_list : 최종 리스트
#     # topactive_list = []
#     # for i in range(len(col_list)):
#     #     topactive_list.append(col_list[i])
#     # for i in range(len(step01_list)):
#     #     topactive_list.append(step01_list[i])
#     # print("topactive_list ", len(topactive_list))
#     # print(topactive_list)

# else:
#     print(response.status_code)

# # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html

# df2 = pd.DataFrame(step01_list)
# print(df2)

# #contentarea > div.box_type_l > table > tbody

title_list.insert(1,data_list[:4])
# print(title_list)
print(set(title_list))