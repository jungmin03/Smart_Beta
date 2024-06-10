import pandas_datareader.data as web
import pandas_datareader.famafrench as ff
import pandas as pd

datasets = ff.get_available_datasets()  # famafrench 패키지에서 get_available_datasets() 함수를 하용하여 이용 가능한 데이터셋을 확인
datasets

df_3_factor = datasets[0]
ds_factors = web.DataReader(df_3_factor, 'famafrench', start='1980-02-01', end='2019-06-30')
ds_factors.keys()
print(ds_factors['DESCR'])
ds_factors[0]

ds_factors[0].index = ds_factors[0].index.strftime('%Y-%m') # 나중에 구할 펀드 수익률과 합치기 위해 인덱스 종류를 변경 / 날짜와 시간을 문자열료 출력하기 위해 strftime() 함수 사용
ds_3_factors = ds_factors[0]


## 펀드(Fidelity Contrafund Fund, FCNTX) 주가를 내려받고 초과수익률 계산
from pandas_datareader import data as web
import pandas as pd
import yfinance as yf

ticker = "FCNTX" 

pxclose = yf.download(ticker, start='1980-01-01',end='2019-06-30', interval='1mo')['Adj Close'] # 지정한 기간동안 펀드의 원간 과거 주가 중 수정주가를 구함
pxclose.index = pxclose.index.strftime('%Y-%m') # 앞서 구한 요인 자료와 합치기 위해 인데스 종류를 변경
ret_data = pxclose.pct_change()[1:] # 수익률 계산
ret_data = pd.DataFrame(ret_data)   # 데이터프레임으로 변경
ret_data.columns=['portfolio']  # 컬럼명을 portfolio로 변경

regress_data = ret_data.merge(ds_3_factors, how='inner', left_index=True, right_index=True) # 회귀분석을 위하여 두개의 데이터프레임을 합침/두 데이터프레임 인덱스를 기준으로 합치는 경우 매개변수 left_index와 right_index를 True로 함 / 합치려는 두 프레임의 컬럼 데이터나 인덱스끼리 서로 일치하는 데이터만 합치는 경우 how 매개변수를 inner로 함

regress_data.rename(columns={"Mkt-RF":"mkt_excess"}, inplace=True)  # 컬럼명 변경

regress_data['port_excess'] = regress_data['portfolio'] - regress_data['RF']    # 초과수익률을 계산하고 port_excess 컬럼을 만들어 저장
regress_data

import statsmodels.api as smf   # 회귀분석과 시계열 처를 위한 데이터 분석 패키지
model = smf.formula.ols(formula = "port_excess ~ mkt_excess + SMB + HML", data = regress_data).fit()    # port_excess를 종속변수로 하고, mkt_excess, SBM, HML을 독립변수로 해서 회귀분석을 실시

print(model.params)
print(model.summary())
