import requests
from bs4 import BeautifulSoup
import pandas as pd

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