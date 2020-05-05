import numpy as np 
import pandas as pd 
import util 
import datetime as dt
import matplotlib.pyplot as plt

def compute_indicators(prices_all,syms=['JPM'],window=20):
	prices = prices_all

	# Compute SMA 
	SMA = prices.rolling(window=window).mean()
	price_SMA = prices / SMA

	# Compute Boellinger Bands 
	std = prices.rolling(window=window).std()
	upper_bb = SMA + (2 * std)
	down_bb  = SMA - (2 * std)
	bb_val = (prices - SMA)/(2 * std)

	# Compute Momentum
	Momentum = (prices/prices.shift(window)) - 1

	# Compute Volatility 
	Volatility = prices.rolling(window=window).std()

	# Compute MACD
	EMA_26 = prices.ewm(span=26).mean()
	EMA_12 = prices.ewm(span=12).mean()
	MACD = EMA_12 - EMA_26

	indicators = pd.DataFrame(index=prices.index)

	indicators['price_SMA'] = price_SMA
	indicators['Upper_BB'] = upper_bb
	indicators['Down_BB'] = down_bb
	indicators['BB_val'] = bb_val
	indicators['Momentum'] = Momentum
	indicators['Volatility'] = Volatility
	indicators['MACD'] = MACD
	#indicators = indicators.dropna()

	return indicators

def author():
	return 'htekgul3'


def test_code():
	start_date = dt.datetime(2008,1,1)
	end_date = dt.datetime(2009,12,31)
	syms = ['JPM']
	dates = pd.date_range(start_date,end_date)
	prices_all = util.get_data(syms, dates)

	plt.figure(0)
	indicators = compute_indicators(prices_all,syms)
	indicators['prices'].plot(label='JPM')
	indicators['SMA'].plot(label='SMA')
	plt.title('Simple Moving Average (SMA)')
	plt.ylabel('Normalized Price')
	plt.legend()
	plt.grid()
	plt.savefig('SMA.png')

	plt.figure(1)
	indicators['Upper_BB'].plot(label='Upper BB')
	indicators['Down_BB'].plot(label='Down BB')
	indicators['prices'].plot(label='JPM')
	indicators['SMA'].plot(label='SMA')
	plt.title('Boellinger Bands')
	plt.legend()
	plt.grid()
	plt.savefig('BB.png')

	plt.figure(2)
	indicators['BB_val'].plot(label='BB Value')
	plt.title('BB Value')
	plt.ylabel('Normalized Price')
	plt.legend()
	plt.grid()
	plt.savefig('BB_Val.png')

	plt.figure(3)
	indicators['Momentum'].plot(label='Momentum')
	indicators['prices'].plot(label='prices')
	plt.title('Momentum')
	plt.legend()
	plt.grid()
	plt.savefig('momentum.png')

	plt.figure(4)
	indicators['Volatility'].plot(label='Volatility')
	indicators['prices'].plot(label='JPM')
	plt.title('Volatility')
	plt.legend()
	plt.grid()
	plt.savefig('volatility.png')
	
	plt.figure(5)
	indicators['MACD'].plot(label='MACD')
	indicators['prices'].plot(label='JPM')
	plt.title('Moving Average Convergence Divergence')
	plt.legend()
	plt.grid()
	plt.savefig('MACD.png')
	return

if __name__ == "__main__":
	test_code()