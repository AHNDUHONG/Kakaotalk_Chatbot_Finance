import requests
from bs4 import BeautifulSoup

url = "https://finance.naver.com/sise/sise_index.naver?code=KOSDAQ"

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    goal = soup.select_one('#now_value')
    goal_str = str(goal.get_text())
    # print(goal.get_text())
    # print(type(goal_str))
    
    goal2 = soup.select_one('#change_value_and_rate')
    # print(goal2.get_text())
    # print(type(goal2))
    goal2_str = str(goal2.get_text())
    # print(goal2_str)
    # print(type(goal2_str))
    # goal2_str_split = goal2_str.split(" ")
    # goal3 = goal2_str_split.insert(0, goal)
    # print(goal3)
    final_goal = goal_str + ' ' + goal2_str
    print(final_goal)
else:
    print(response.status_code)