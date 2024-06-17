import pandas as pd
import numpy as np
import pandas_datareader.data as web
from datetime import datetime
from sqlalchemy import create_engine
import pymysql



# 1. 데이터 가져오기
engine = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/stock_db')
con = pymysql.connect(user='root',
                    passwd='1234',
                    host='127.0.0.1',
                    db='stock_db',
                    charset='utf8')
mycursor = con.cursor()

# 티커리스트 불러오기(기준일이 최대, 즉, 최근일 기준 보통주에 해당하는 ticker_list만 불러온다)
kor_stock = pd.read_sql("""
select * from kor_ticker
where 기준일 = (select max(기준일) from kor_ticker) 
    and 종목구분 = '보통주';
""", con=engine)

ticker_list = kor_stock.iloc[:, 0]
ticker_list = ticker_list.to_list()

ticker_data = {}

start_date = '2000-01-01'
end_date = '2016-12-31'

range(len(ticker_list))

for i in range(len(ticker_list)):
    i
    ticker_list[i]
    data = web.DataReader(ticker_list[i], 'naver', start_date, end_date)['Close']
    data

web.DataReader('472850', 'naver') 

data
    ticker_list[i]
    data

data = web.DataReader(ticker_list[2], 'naver', start_date, end_date)['Close']
data

# 월별 데이터로 변환
monthly_data = data.resample('M').last()
monthly_data = monthly_data.to_frame()
monthly_data['Close'] = monthly_data['Close'].astype('float')


# 2. 월별 수익률 계산
monthly_returns = monthly_data.pct_change().dropna()

# 3. 과거 5년(60개월) 기준 월별 수익률의 표준편차를 계산
rolling_std_dev = monthly_returns.rolling(window=60).std()

rolling_std_dev
monthly_returns




