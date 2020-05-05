import datetime as dt  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
import pandas as pd 
import numpy as np 		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
import math
from marketsimcode import *
import matplotlib.pyplot as plt
import yfinance as yf
import yahoofinancials
from indicators import compute_indicators
from sklearn.tree import DecisionTreeClassifier


def get_stock_data(symbol,sd=dt.datetime(2018,1,1),ed=dt.datetime(2019,1,1)):
	stock_df = yf.download(symbol, start=sd, end=ed,progress=False)
	adj_close = stock_df['Adj Close']
	return adj_close.to_frame()

def get_indicator_data(data,symbol,window,train=True):
	indicators = compute_indicators(data,symbol,window=window)
	indicators.fillna(0,inplace=True)
	indicator_data = indicators.copy()
	if train:
		indicator_data = indicator_data[:-3]
	indicator_data.drop('Upper_BB', axis=1, inplace=True)
	indicator_data.drop('Down_BB', axis=1, inplace=True)
	#indicator_data.drop('Volatility', axis=1, inplace=True)
	#indicator_data.drop('Momentum', axis=1, inplace=True)
	#indicator_data.drop('BB_val', axis=1, inplace=True)
	#indicator_data.drop('MACD', axis=1, inplace=True)
	indicator_data = indicator_data.values
	return indicator_data

def get_labels(prices,market_impact):
	labels = np.zeros(prices.shape[0]-3)
	for i in range(prices.shape[0]-3):
		ret = (prices.values[i+3] - prices.values[i])
		if ret / prices.values[i] < (-1*market_impact - 0.02):
			labels[i] = -1 # SELL
		elif ret / prices.values[i] > (market_impact + 0.02):
			labels[i] = 1 # BUY
	return labels

def create_trades_df(prices,symbol,Y_test):
	trades = pd.DataFrame(index = prices.index) 
	trades[symbol] = 0
	shares = 0
	for i in range(prices.shape[0]-3):
		if shares == 0 and Y_test[i] == 1:
			trades.iloc[i,0] = 20
			shares = 20
		elif shares > 0 and Y_test[i] == -1:
			trades.iloc[i,0] = -20
			shares = 0
	return trades



# Provide a set of stocks and get historical data
symbols = ['TQQQ']

sd_train = dt.datetime(2015,1,1)
ed_train = dt.datetime(2019,1,1)
sd_test = dt.datetime(2019,5,5)
ed_test = dt.datetime(2020,1,1)

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
	labels_test = clf.predict(indicators_test[:-3])
	labels_true = get_labels(stock_df_test, market_impact=0.005)
	
	trades_df = create_trades_df(stock_df_test,symbol,labels_test)
	orders = trades2orders(trades_df,symbol)
	strategy_pval = compute_portvals(stock_df_test,orders,start_val=3000,commission=0.0,impact=0.005)
	crb,adrb,sddrb,srb = compute_stats(strategy_pval)
	strategy_pval = strategy_pval / strategy_pval[0]

	print(labels_test)

	print(symbol)  
	print(orders) 		     			  		 			     			  	  		 	  	 		 			  		  			
	print("Cumulative Return: " + str(crb))
	print("Stdev of daily returns: " + str(sddrb))
	print("Average Daily Return: " + str(adrb))
	print("Sharpe Ratio: " + str(srb))	
	print()
	print()

	plt.figure(0)
	plt.plot(strategy_pval,'r',label='StrategyLearner')
	plt.grid()
	plt.legend()
	plt.title(symbol)
	plt.show()








