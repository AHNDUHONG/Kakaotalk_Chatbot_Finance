import pandas as pd
import numpy as np

# 파일 경로 설정
Location = "C:/Users/dksen/Desktop/Project_ADH/주식프로젝트/Kakaotalk_Chatbot_Finance/bash/Finance_commission_file"
File = '주식거래 수수료_20220520.xls'

# 추출 및 변환 코드
data_pd = pd.read_excel('{}/{}'.format(Location, File),
            header = None, index_col = None, names = None)
data_np = pd.DataFrame.to_numpy(data_pd)

kor = 105
hanhwa = 52
hana = 39
kiwoom = 84
samsung = 101
# 종목명, 필요한 데이터 등을 리스트화 하여 출력하는 함수 생성 
def D_F(a):
    if a == 105:        # 한국투자증권
        kor_f = []
        kor_f.append(data_pd.iloc[a,0])
        kor_f.append(data_pd.iloc[a,3])
        for i in range(5,9):
            kor_f.append(data_pd.iloc[a,i])
        print(f'종목명 : {kor_f[0]}\n기준금액 : {kor_f[1]}\n오프라인 개설 수수료 : {kor_f[2]}원\nHTS 수수료 : {kor_f[3]}원\nARS 수수료 : {kor_f[4]}원\nMTS 수수료 : {kor_f[5]}원')

    elif a == 52:       # 한화투자증권
        hanhwa_f = []
        hanhwa_f.append(data_pd.iloc[a,0])
        hanhwa_f.append(data_pd.iloc[a,3])
        for i in range(5,9):
            hanhwa_f.append(data_pd.iloc[a,i])
        print(f'종목명 : {hanhwa_f[0]}\n기준금액 : {hanhwa_f[1]}\n오프라인 개설 수수료 : {hanhwa_f[2]}원\nHTS 수수료 : {hanhwa_f[3]}원\nARS 수수료 : {hanhwa_f[4]}원\nMTS 수수료 : {hanhwa_f[5]}원')

    elif a == 39:       # 하나금융투자
        hana_f = []
        hana_f.append(data_pd.iloc[a,0])
        hana_f.append(data_pd.iloc[a,3])
        for i in range(5,9):
            hana_f.append(data_pd.iloc[a,i])
        print(f'종목명 : {hana_f[0]}\n기준금액 : {hana_f[1]}\n오프라인 개설 수수료 : {hana_f[2]}원\nHTS 수수료 : {hana_f[3]}원\nARS 수수료 : {hana_f[4]}원\nMTS 수수료 : {hana_f[5]}원')

    elif a == 84:       # 키움증권
        kiwoom_f = []
        kiwoom_f.append(data_pd.iloc[a,0])
        kiwoom_f.append(data_pd.iloc[a,3])
        for i in range(5,9):
            kiwoom_f.append(data_pd.iloc[a,i])
        print(f'종목명 : {kiwoom_f[0]}\n기준금액 : {kiwoom_f[1]}\n오프라인 개설 수수료 : {kiwoom_f[2]}원\nHTS 수수료 : {kiwoom_f[3]}원\nARS 수수료 : {kiwoom_f[4]}원\nMTS 수수료 : {kiwoom_f[5]}원')

    elif a == 101:      # 삼성증권
        samsung_f = []
        samsung_f.append(data_pd.iloc[a,0])
        samsung_f.append(data_pd.iloc[a,3])
        for i in range(5,9):
            samsung_f.append(data_pd.iloc[a,i])
        print(f'종목명 : {samsung_f[0]}\n기준금액 : {samsung_f[1]}\n오프라인 개설 수수료 : {samsung_f[2]}원\nHTS 수수료 : {samsung_f[3]}원\nARS 수수료 : {samsung_f[4]}원\nMTS 수수료 : {samsung_f[5]}원')
        

# 출력
D_F(kiwoom)
