"""MC2-P1: Market simulator.                                                                                        
                                                                                        
Copyright 2018, Georgia Institute of Technology (Georgia Tech)                                                                                        
Atlanta, Georgia 30332                                                                                        
All Rights Reserved                                                                                       
                                                                                        
Template code for CS 4646/7646                                                                                        
                                                                                        
Georgia Tech asserts copyright ownership of this template and all derivative                                                                                        
works, including solutions to the projects assigned in this course. Students                                                                                        
and other users of this template code are advised not to share it with others                                                                                       
or to make it available on publicly viewable websites including repositories                                                                                        
such as github and gitlab.  This copyright statement should not be removed                                                                                        
or edited.                                                                                        
                                                                                        
We do grant permission to share solutions privately with non-students such                                                                                        
as potential employers. However, sharing with other current or future                                                                                       
students of CS 7646 is prohibited and subject to being investigated as a                                                                                        
GT honor code violation.                                                                                        
                                                                                        
-----do not edit anything above this line---                                                                                        
                                                                                        
Student Name: Tucker Balch (replace with your name)                                                                                       
GT User ID: tb34 (replace with your User ID)                                                                                        
GT ID: 900897987 (replace with your GT ID)                                                                                        
"""                                                                                       
                                                                                        
import pandas as pd                                                                                       
import numpy as np                                                                                        
import datetime as dt                                                                                       
import os                                                                                       
from util import get_data, plot_data                                                                                        
                                      
def compute_stats(port_val):
    daily_ret = (port_val/port_val.shift(1)) - 1   
    cr = (port_val[-1]/port_val[0]) - 1
    adr = daily_ret.mean()
    sddr = daily_ret.std()
    sr = np.sqrt(252.0) * ((daily_ret - 0.0).mean() / sddr) 
    return cr,adr,sddr,sr

def trades2orders(df_trades,symbol):
  trades = pd.DataFrame(columns=['ORDER', 'Symbol', 'Shares'],index=df_trades.index)
  for i in range(df_trades.shape[0]):
    if df_trades.iloc[i,0] > 0:
      trades.iloc[i,:] = ['BUY',symbol,df_trades.iloc[i,0]]
    if df_trades.iloc[i,0] < 0:
      trades.iloc[i,:] = ['SELL',symbol,df_trades.iloc[i,0]]
  orders = trades.dropna()
  return orders
                                                      
def compute_portvals(data,orders, start_val = 100000, commission=0.0, impact=0.0):                                                                                       
    # this is the function the autograder will call to test your code                                                                                       
    # NOTE: orders_file may be a string, or it may be a file object. Your                                                                                       
    # code should work correctly with either input                                                                                        
    # TODO: Your code here                                                                                        
    # Read unique symbols
    symbols = list(set(orders['Symbol']))
    # Read all the trading dates and sort 
    
    # Create the df prices and add CASH column of all ones 
    df_prices = data 
    df_prices['Cash'] = np.ones(df_prices.shape[0])
    # Create the df trades and fill it in accordingly
    df_trades = df_prices.copy()
    df_trades = df_trades * 0.0 # make it all zero
    multiplier = 0
    for date_i,row_i in orders.iterrows():
      symbol = row_i[1]
      buy_sell = row_i[0]
      shares = row_i[2]

      if buy_sell == 'SELL':
        multiplier = -1
      if buy_sell == 'BUY':
        multiplier = 1

      df_trades.loc[date_i,symbol] += (multiplier * shares)
      df_trades.loc[date_i,'Cash'] += (shares*-multiplier)*df_prices[symbol].loc[date_i]
      df_trades.loc[date_i,'Cash'] -= commission
      df_trades.loc[date_i,'Cash'] -= shares * df_prices[symbol].loc[date_i] * impact
    
    # Create the df holdings and fill it in accordingly
    df_holdings = df_trades.copy()
    df_holdings = df_holdings * 0.0 # make it all zero

    df_holdings.loc[df_prices.index[0],'Cash'] = start_val
    df_holdings += df_trades
    df_holdings = df_holdings.cumsum()

    # Create the df values
    df_values = df_prices * df_holdings

    # Create the final data frame, the portfolio values
    df_portval = df_values.sum(axis = 1)
                                                                                        
    return df_portval 

def author():
    return 'htekgul3'                                                          
                                                                                        
if __name__ == "__main__":                                                                                        
    print('You are not supposed to do this.')                                                                                       
