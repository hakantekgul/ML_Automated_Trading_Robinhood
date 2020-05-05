from Robinhood import Robinhood 
import datetime as dt  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
import pandas as pd 
import numpy as np 		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
from marketsimcode import *
import matplotlib.pyplot as plt
import yfinance as yf
import yahoofinancials
from indicators import compute_indicators
from sklearn.tree import DecisionTreeClassifier


def get_stock_data(symbol,sd=dt.datetime(2018,1,1),ed=dt.datetime(2019,1,1)):
	# Read historical stock data from Yahoo Finance
	stock_df = yf.download(symbol, start=sd, end=ed,progress=False)
	# Should be Adjusted Close!
	adj_close = stock_df['Adj Close']
	return adj_close.to_frame()

def get_indicator_data(data,symbol,window,train=True):
	# Compute indicators, which are features
	indicators = compute_indicators(data,symbol,window=window)
	indicators.fillna(0,inplace=True)
	indicator_data = indicators.copy()
	if train:
		indicator_data = indicator_data[:-3]

	# Uncomment below to try different set of features
	indicator_data.drop('Upper_BB', axis=1, inplace=True)
	indicator_data.drop('Down_BB', axis=1, inplace=True)
	#indicator_data.drop('Volatility', axis=1, inplace=True)
	#indicator_data.drop('Momentum', axis=1, inplace=True)
	#indicator_data.drop('BB_val', axis=1, inplace=True)
	#indicator_data.drop('MACD', axis=1, inplace=True)
	indicator_data = indicator_data.values # to numpy array
	return indicator_data

def get_labels(prices,market_impact):
	# If return after 3 days is high enough, it is a BUY. If it is low, it is a SELL.
	labels = np.zeros(prices.shape[0]-3)
	# 0 label is DO NOTHING
	for i in range(prices.shape[0]-3):
		ret = (prices.values[i+3] - prices.values[i])
		if ret / prices.values[i] < (-1*market_impact - 0.02):
			labels[i] = -1 # SELL
		elif ret / prices.values[i] > (market_impact + 0.02):
			labels[i] = 1 # BUY
	return labels

def create_trades_df(prices,symbol,Y_test):
	# Based on labels, create trades dataframe
	trades = pd.DataFrame(index = prices.index) 
	trades[symbol] = 0
	shares = 0
	for i in range(prices.shape[0]-3):
		if shares == 0 and Y_test[i] == 1:
			trades.iloc[i,0] = 20
			shares = 20
		elif shares > 0 and Y_test[i] == 0:
			trades.iloc[i,0] = -20
			shares = 0
	return trades


# First, login to Robinhood with your credentials
# Assuming 2FA is ON

QR = "123456789qwertyu"
my_trader = Robinhood()
my_trader.login(username="username@gmail.com", password="P@ssw0rd", qr_code=QR)

# Provide a set of stocks and get historical data
symbols = ['TQQQ']

# Train for the last 5 years
sd_train = dt.datetime(2015,1,1)
tod = dt.datetime.now()
d = dt.timedelta(days = 30) # 30 days just to make sure indicators are computed fine
a = tod - d
sd_test = a
ed_test = dt.datetime.date(dt.datetime.now())
ed_train = sd_test

for symbol in symbols:
	stock_df_train = get_stock_data(symbol,sd_train,ed_train)
	stock_df_train.columns = [symbol]
	indicators_train = get_indicator_data(stock_df_train,symbol,window=5,train=True)
	labels_train = get_labels(stock_df_train,market_impact=0.005)	

	stock_df_test = get_stock_data(symbol,sd_test,ed_test)
	stock_df_test.columns = [symbol]
	indicators_test = get_indicator_data(stock_df_test,symbol,window=5,train=False)

	clf = DecisionTreeClassifier(max_depth=5)
	clf.fit(indicators_train, labels_train)
	labels_test = clf.predict(indicators_test[-1].reshape(1,-1))
	labels_true = get_labels(stock_df_test, market_impact=0.005)

	# Read the file to get your current shares from Robinhood. 
	# IF using this first time, you need to manually create filename and add number of shares as .txt file
	f_name = symbol + str('.txt')
	f = open(f_name, 'r')
	nums = f.readlines()
	nums = [int(i) for i in nums]
	shares = nums[0]
	f.close()

	# Strategy, if it is a BUY signal, just buy 20 shares. If it is a SELL, sell the shares if you have any.
	if shares == 0 and labels_test[-1] == 1:
		print('BUYING 20 '+ str(symbol)+' ...')
		stock_instrument = my_trader.instruments(symbol)[0]
		#buy_order = my_trader.place_market_buy_order(stock_instrument['url'], symbol, 'GFD', 20)
		shares = 20
		with open(f_name,'w') as f:
			f.write(str(shares))

	elif shares > 0 and labels_test[-1] == -1:
		print('SELLING ALL '+str(symbol)+' ...')
		stock_instrument = my_trader.instruments(symbol)[0]
		#sell_order = my_trader.place_market_sell_order(stock_instrument['url'], symbol, 'GFD', 20)
		shares = 0
		with open(f_name,'w') as f:
			f.write(str(shares))

	else: 
		print('DOING NOTHING')




