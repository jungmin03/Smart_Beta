# 요인 데이터 구하기
import pandas_datareader.data as web  # module for reading datasets directly from the web
import pandas_datareader.famafrench as ff 

datasets = ff.get_available_datasets()  # famafrench 패키지에서 get_available_datasets() 함수를 하용하여 이용 가능한 데이터셋을 확인
print('No. of datasets:{0}'.format(len(datasets)))  # len() 함수를 이용하여 datasets에 이용 가능한 데이터셋 개수 확인
print(datasets)


## 10개 인더스트리 포트폴리오에 대한 데이터셋 받기
df_10_industry = [dataset for dataset in datasets if '10' in dataset and 'Industry' in dataset] # 데이터셋 이름에서 10과 industry가 들어간 데이터셋만 찾아서 df_10_industry 변수에 저장
print(df_10_industry)

ds_industry = web.DataReader( df_10_industry[0], 'famafrench', start = '2017-06-23', end = '2019-11-01')    # DataReader() 함수를 이용해 첫번째 데이터 셋(10_Industry_Portfolios)의 '2017-06-23'부터 '2019-11-01'까지 데이터를 다운로드
print(type(ds_industry))    # type() 함수를 사용해서 내려받은 데이터셋의 데이터형을 확인
ds_industry.keys()  # ds_industry의 key값을 출력

print(ds_industry['DESCR']) # 데이터셋에 대한 설명(DESCR)을 출력
ds_industry[0].head()


## 5개 요인 데이터셋 받기
df_5_factor = [dataset for dataset in datasets if '5' in dataset and 'Factor' in dataset]   # 데이터셋 이름 중 5와 Factor가 들어간 데이터셋만 고른 후 df_5_factor 변수에 저장
print(df_5_factor)

ds_factors = web.DataReader(df_5_factor[0], 'famafrench', start='2017-06-23', end='2019-11-01') # 데이터셋 중 첫번째 데이터 셋인 'F-F_Research_Data_5_Factors_2*3을 내려받고 지정한 기간동안의 자료 다운로드
print('\nKEYS\n{0}'.format(ds_factors.keys()))  # 데이터셋의 키 값 출력
print('DATASET DESCRIPTION \n {0}'.format(ds_factors['DESCR'])) # 데이터셋에 대한 설명(DESCR)을 출력
ds_factors[0].head()





