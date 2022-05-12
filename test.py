# # 삼성전자 ==> 005930
# # 카카오 ==> 035720
# # 한화생명 ==> 088350
# # 애플 ==> AAPL

# # Open ==> 시작가
# # High ==> 최고가격
# # Low ==> 최저가격
# # Close ==> 마감가
# # Volume ==> 거래량


# # pip install pandas_datareader 필요
import pandas_datareader.data as web


# # 국내 주식
# # naver finance에서 추출

samsung = web.DataReader('005930', 'naver')
print(samsung)
print(samsung.info())



# # 해외 주식
# # yahoo finance에서 추출

apple = web.get_data_yahoo('AAPL')
print(apple)
print(apple.info())