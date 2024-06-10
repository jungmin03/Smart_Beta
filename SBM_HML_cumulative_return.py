import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as web

# # Fama-French 3-factor 데이터 다운로드
# df_3_factor = 'F-F_Research_Data_Factors'
# ds_factors = web.DataReader(df_3_factor, 'famafrench', start='1980-02-01', end='2019-06-30')

# # 데이터셋의 키 확인
# print(ds_factors.keys())

# # 데이터셋 설명 확인
# print(ds_factors['DESCR'])

# # 필요한 데이터 가져오기
# ds_3_factors = ds_factors[0]

# # 인덱스 포맷 변경
# ds_3_factors.index = ds_3_factors.index.to_timestamp()

# # SMB와 HML 누적 수익률 계산
# ds_3_factors['SMB'] = ds_3_factors['SMB'] / 100  # 퍼센트로 표시된 데이터를 소수로 변환
# ds_3_factors['HML'] = ds_3_factors['HML'] / 100

# ds_3_factors['Cumulative_SMB'] = (1 + ds_3_factors['SMB']).cumprod() - 1    # 누적수익률 계산 / 누적곱을 반환하는 cumprod() 매서드 활용
# ds_3_factors['Cumulative_HML'] = (1 + ds_3_factors['HML']).cumprod() - 1

# ds_3_factors

# # 그래프 그리기
# plt.figure(figsize=(14, 7))
# plt.plot(ds_3_factors.index, ds_3_factors['Cumulative_SMB'], label='SMB Cumulative Return', color='blue')
# plt.plot(ds_3_factors.index, ds_3_factors['Cumulative_HML'], label='HML Cumulative Return', color='red')
# plt.xlabel('Date')
# plt.ylabel('Cumulative Return')
# plt.title('SMB & HML Cumulative Return')
# plt.legend()
# plt.grid(True)
# plt.show()



import pandas as pd
import pandas_datareader.data as web
import pandas_datareader.famafrench as ff
import matplotlib.pyplot as plt

# 이용 가능한 데이터셋 확인 및 필터링
datasets = ff.get_available_datasets()
filtered_datasets = [ds for ds in datasets if '3_Factors' in ds and 'Daily' not in ds and ds != "F-F_Research_Data_5_Factors_2x3"]

print(f'Number of filtered datasets: {len(filtered_datasets)}')
print('Filtered datasets:', filtered_datasets)

# 데이터 가져오기와 인덱스 변환을 수행하는 함수
def get_and_convert_data(dataset_name, start_date, end_date):
    ds = web.DataReader(dataset_name, 'famafrench', start=start_date, end=end_date)
    ds[0].index = ds[0].index.to_timestamp()
    return ds[0]

# 시작 및 종료 날짜 설정
start_date = '1980-02-01'
end_date = '2019-06-30'

# 각 데이터셋에 대한 데이터 가져오기 및 변환
data_frames = {name: get_and_convert_data(name, start_date, end_date) for name in filtered_datasets[:7]}

# SMB와 HML 누적 수익률 계산
for name, df in data_frames.items():
    df['SMB'] = df['SMB'] / 100
    df['HML'] = df['HML'] / 100
    df['Cumulative_SMB'] = (1 + df['SMB']).cumprod() - 1
    df['Cumulative_HML'] = (1 + df['HML']).cumprod() - 1

# 특정 열 선택 및 결합
df_Cum_SMB = pd.concat([df['Cumulative_SMB'] for df in data_frames.values()], axis=1)

# 열 이름 지정
df_Cum_SMB.columns = [name for name in data_frames.keys()]

# 그래프 그리기
plt.figure(figsize=(14, 7))
for column in df_Cum_SMB.columns:
    plt.plot(df_Cum_SMB.index, df_Cum_SMB[column], label=column)

plt.xlabel('Date')
plt.ylabel('Cumulative SMB')
plt.title('Regional SMB Factor Cumulative Return')
plt.legend()
plt.grid(True)
plt.show()




