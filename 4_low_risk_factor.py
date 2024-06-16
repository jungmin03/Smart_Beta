import pandas as pd
import numpy as np
import yfinance as yf
from sqlalchemy import create_engine
import pymysql
import pandas_datareader.data as web


def calculate_monthly_returns(data):
    """
    월별 수익률을 계산하는 함수.
    """
    monthly_data = data.resample('M').last()  # 월별 마지막 거래일 데이터로 리샘플링
    monthly_returns = monthly_data['Adj Close'].pct_change().dropna()
    return monthly_returns

def calculate_arithmetic_mean(returns):
    """
    수익률의 산술평균을 계산하는 함수.
    """
    return returns.mean()

def calculate_geometric_mean(returns):
    """
    수익률의 기하평균을 계산하는 함수.
    """
    return (np.prod(1 + returns))**(1/len(returns)) - 1

def calculate_rolling_std(returns, window):
    """
    과거 window 기간(개월) 기준의 월별 수익률 표준편차를 계산하는 함수.
    """
    rolling_std = returns.rolling(window=window).std().dropna()
    return rolling_std


# KOSPI 종목 리스트를 가져오는 함수 (예제에서는 파일에서 읽기)
def get_kospi_tickers():
    engine = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/stock_db')
    con = pymysql.connect(user='root',
                        passwd='1234',
                        host='127.0.0.1',
                        db='stock_db',
                        charset='utf8')
    mycursor = con.cursor()

    # 티커리스트 불러오기(기준일이 최대, 즉, 최근일 기준 보통주에 해당하는 ticker_list만 불러온다)
    kor_ticker_list = pd.read_sql("""
    select * from kor_ticker
    where 기준일 = (select max(기준일) from kor_ticker) 
        and 종목구분 = '보통주';
    """, con=engine)
    
    return kor_ticker_list

get_kospi_tickers()

# 데이터 가져오기
start_date = '2000-01-01'
end_date = '2016-12-31'
tickers = get_kospi_tickers()
tickers

# 결과를 저장할 데이터프레임 초기화
all_rolling_stds_arithmetic = pd.DataFrame()
all_rolling_stds_geometric = pd.DataFrame()


tickers

tickers_list = tickers.values.tolist()
tickers_list


tickers_list[1]

len(tickers_list)


for i in range(len(tickers_list)):
    test = tickers[i, 0]


for ticker in tickers:
    # yfinance에서 데이터 가져오기
    # data = yf.download(ticker, start=start_date, end=end_date)
    data = web.DataReader(ticker, 'naver')

    # 월별 수익률 계산
    monthly_returns = calculate_monthly_returns(data)
    
    # 과거 5년(60개월) 기준의 월별 수익률 표준편차 계산
    window = 60
    
    # 산술평균 수익률 표준편차 계산
    arithmetic_rolling_std = calculate_rolling_std(monthly_returns, window)
    all_rolling_stds_arithmetic[ticker] = arithmetic_rolling_std
    
    # 기하평균 수익률 표준편차 계산
    geometric_rolling_std = monthly_returns.rolling(window=window).apply(calculate_geometric_mean).dropna().rolling(window=window).std().dropna()
    all_rolling_stds_geometric[ticker] = geometric_rolling_std

# 결과 출력
print("산술평균 수익률 표준편차:")
print(all_rolling_stds_arithmetic)

print("\n기하평균 수익률 표준편차:")
print(all_rolling_stds_geometric)

# 결과를 파일로 저장 (선택 사항)
all_rolling_stds_arithmetic.to_csv('arithmetic_rolling_std_60_months.csv', index=True)
all_rolling_stds_geometric.to_csv('geometric_rolling_std_60_months.csv', index=True)
