from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# # 로딩이 필요 할 때 time 라이브러리 사용 필요
## import time


def search_kospi(): 
    # print("hello")


    driver = webdriver.Chrome()
    driver.get("https://finance.naver.com/sise/sise_index.naver?code=KOSPI")

    ## target1 : 코스피 지수
    fir= "now_value"
    # target1= driver.find_element_by_css_selector(fir).text
    target1 = driver.find_element_by_id(fir).text
    print(target1)

    ## target2 : 전일 대비
    sec= ".fluc"
    target2= driver.find_elements_by_css_selector(sec)[0].text
    # print(target2)
    
    # print(target2.split(" "))
    # print(target2)
    target2_split = target2.split(" ")
    target2_split.insert(0, target1)
    print(target2_split)

  
    # # 종료 단계
    driver.close()


    print("kospi end...")

search_kospi()

def search_kosdaq(): 
    # print("kosdaq hello")

    driver = webdriver.Chrome()
    driver.get("https://finance.naver.com/sise/sise_index.naver?code=KOSDAQ")

    ## target1 : 코스닥 지수
    fir= "now_value"
    # target1= driver.find_element_by_css_selector(fir).text
    target1 = driver.find_element_by_id(fir).text
    print(target1)

    ## target2 : 전일 대비
    sec= ".fluc"
    target2= driver.find_elements_by_css_selector(sec)[0].text
    # print(target2)
    
    # print(target2.split(" "))
    # print(target2)
    target2_split = target2.split(" ")
    target2_split.insert(0, target1)
    print(target2_split)

    # # 종료 단계
    driver.close()


    print("kosdaq end...")
search_kosdaq()
