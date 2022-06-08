from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas_datareader.data as web
# import csv
# # 로딩이 필요 할 때 time 라이브러리 사용 필요
import time

# # 종목 검색하기
def search_item(item):
    driver = webdriver.Chrome()
    driver.get("https://www.ktb.co.kr/trading/popup/itemPop.jspx")

    item_name = item

    # # target_search : 종목명 검색
    fir= ".input_txt"
    target1= driver.find_element_by_css_selector(fir)
    target1.send_keys(item_name)
    target1.send_keys(Keys.RETURN)


    try:
        sec= "td"
        target2= driver.find_elements_by_css_selector(sec)[0].text
        target3= driver.find_elements_by_css_selector(sec)[1].text
        # # 확인 단계
        print(target2)
        print(target3)

        # # 국내 주식 검색
        # # naver finance에서 추출
        item_code = target2
        target_data = web.DataReader(item_code, 'naver')
        last = (target_data.shape[0])
        print(target_data.iloc[last - 1])

    # # 이름을 잘못 입력했을때의 예외 처리
    except IndexError:
        print(item_name, "의 ", target2)

    # # 종료 단계
    driver.close()
    print("end...")

# # 검색 상위 30개
def search_top30():
    driver = webdriver.Chrome()
    driver.get("https://finance.naver.com/sise/lastsearch2.naver")

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

        if (divmod(i, 10)[1] == 3):
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
    search_top30_list = []
    search_top30_list.append(col_list)
    for i in range(len(target_list)):

        search_top30_list.append(target_list[i])
    print(search_top30_list)

    # # 종료 단계
    driver.close()
    print("end...")

# # 거래 상위 100개
def active_top100():
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

    # # 종료 단계
    driver.close()
    print("end...")


while True:
    active = input("실행해주세요 ")
    if active == "1":
        search_top30()
    elif active == "2":
        active_top100()
    else:
        search_item(active)