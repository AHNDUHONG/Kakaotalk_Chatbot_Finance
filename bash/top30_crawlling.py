from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
# # 로딩이 필요 할 때 time 라이브러리 사용 필요
import time

driver = webdriver.Chrome()
driver.get("https://finance.naver.com/sise/lastsearch2.naver")

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

# # target2와 target1을 합치기
target_list= []

for i in range(len(target1)):
    target_list.append([])
    target_list[i].append(target1[i].text)

    for j in range(len(target2)):
        if divmod(j, 10)[0] == i:
            target_list[i].append(target2[j])

# # 확인 단계
print(target_list)
print(len(target_list))
print(len(target1))
print(len(target2))

# # 저장 단계
with open('target_list.csv','w', encoding = 'utf8') as file :

    write = csv.writer(file)
    write.writerows(target_list)

# 종료 단계
driver.close()
print("end...")