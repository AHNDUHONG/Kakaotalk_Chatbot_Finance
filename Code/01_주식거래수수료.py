import pandas as pd
import numpy as np
import csv
# 파일 경로 설정
Location = "C:/Users/dksen/Desktop/Project_ADH/chatbot_project/Finance_Project/qwe/Finance_commission_file"
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
        for i in range(5,9):
            kor_f.append(data_pd.iloc[a,i])
        print(f'종목명 : {kor_f[0]}\n오프라인 개설 수수료 : {kor_f[1]}원\nHTS 수수료 : {kor_f[2]}원\nARS 수수료 : {kor_f[3]}원\nMTS 수수료 : {kor_f[4]}원')
        return kor_f

    elif a == 52:       # 한화투자증권
        hanhwa_f = []
        hanhwa_f.append(data_pd.iloc[a,0])
        for i in range(5,9):
            hanhwa_f.append(data_pd.iloc[a,i])
        print(f'종목명 : {hanhwa_f[0]}\n오프라인 개설 수수료 : {hanhwa_f[1]}원\nHTS 수수료 : {hanhwa_f[2]}원\nARS 수수료 : {hanhwa_f[3]}원\nMTS 수수료 : {hanhwa_f[4]}원')
        return hanhwa_f

    elif a == 39:       # 하나금융투자
        hana_f = []
        hana_f.append(data_pd.iloc[a,0])
        for i in range(5,9):
            hana_f.append(data_pd.iloc[a,i])
        print(f'종목명 : {hana_f[0]}\n오프라인 개설 수수료 : {hana_f[1]}원\nHTS 수수료 : {hana_f[2]}원\nARS 수수료 : {hana_f[3]}원\nMTS 수수료 : {hana_f[4]}원')
        return hana_f

    elif a == 84:       # 키움증권
        kiwoom_f = []
        kiwoom_f.append(data_pd.iloc[a,0])
        for i in range(5,9):
            kiwoom_f.append(data_pd.iloc[a,i])
        print(f'종목명 : {kiwoom_f[0]}\n오프라인 개설 수수료 : {kiwoom_f[1]}원\nHTS 수수료 : {kiwoom_f[2]}원\nARS 수수료 : {kiwoom_f[3]}원\nMTS 수수료 : {kiwoom_f[4]}원')
        return kiwoom_f

    elif a == 101:      # 삼성증권
        samsung_f = []
        samsung_f.append(data_pd.iloc[a,0])
        for i in range(5,9):
            samsung_f.append(data_pd.iloc[a,i])
        print(f'종목명 : {samsung_f[0]}\n오프라인 개설 수수료 : {samsung_f[1]}원\nHTS 수수료 : {samsung_f[2]}원\nARS 수수료 : {samsung_f[3]}원\nMTS 수수료 : {samsung_f[4]}원')
        return samsung_f


# 출력
list = [['종목명', '오프라인', 'HTS', 'ARS', 'MTS']]
list.append(D_F(kor))
list.append(D_F(hanhwa))
list.append(D_F(hana))
list.append(D_F(kiwoom))
list.append(D_F(samsung))
print(list)


# # # 저장 단계
with open('Finance_commission.csv','w', encoding = 'utf8') as file :

    write = csv.writer(file)
    write.writerows(list)

# def find(a):
#     csv_test = pd.read_csv('Finance_commission.csv')
#     for i in range(csv_test.shape[0]):
#         if csv_test.loc[:,'종목명'].iloc[i] == a:
#             print(csv_test.iloc[i])
# dataframe = pd.DataFrame(list, columns= ['종목명', '기준금액', '오프라인 개설 수수료', 'HTS 수수료', 'ARS 수수료', 'MTS 수수료'])
# dataframe.to_csv(header=False, index = False)
