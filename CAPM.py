import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import FinanceDataReader as fdr
import statsmodels.api as sm

ticker = '005930'
market = 'KS11'

# 삼성전자와 KOSPI 데이터 다운로드
stock_data = fdr.DataReader(ticker)
stock_data = stock_data.astype('float')
stock_data.info()

market_data = fdr.DataReader(market)
market_data = market_data.astype('float')
market_data.info()

# 2000년부터 2016년까지 데이터 슬라이싱
stock_df = stock_data.loc['2000-01-01':'2016-12-31']
market_df = market_data.loc['2000-01-01':'2016-12-31']

stock_df.info()
market_df.info()

# 월간 수익률 계산
stock_data['stock_Monthly Returns'] = stock_df['Close'].pct_change()
market_data['market_Monthly Returns'] = market_df['Close'].pct_change()

# 수익률 데이터 정리
data = pd.DataFrame({
    'Stock Monthly Return' : stock_data['stock_Monthly Returns'],
    'Market Monthly Return' : market_data['market_Monthly Returns']
}).dropna()

data

# 회귀분석
x = data['Market Monthly Return']
y = data['Stock Monthly Return']
x = sm.add_constant(x)
model = sm.OLS(y, x).fit()
print(model.summary())

# 그래프 그리기
plt.figure(figsize=(10, 6))
plt.scatter(data['Market Monthly Return'], data['Stock Monthly Return'], alpha=0.5)
plt.plot(data['Market Monthly Return'], model.predict(x), color='black', label='회귀선')
plt.title('Market vs. Stock Return')
plt.xlabel('Market Monthly Return')
plt.ylabel('Stock Monthly Return')
plt.grid(True)
plt.show()
