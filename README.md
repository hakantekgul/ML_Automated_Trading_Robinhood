# Automated_Trading_Robinhood

> Machine Learning based Automated Trading with Robinhood app

The basic idea is to read historical data and compute indicators as our features for classification. The BUY and SELL signals are created based on the future peak of historical data. If the cumulative return of a stock after 3 days into the future is high enough, it is a BUY signal. If it is low, it is considered to be a SELL signal. If it is pretty much the same, we DO NOTHING. Basic sci-kit learn ML models are used. 

## Installation

OS X & Linux:
First, download the unofficial Robinhood API that lets you login and place market orders. See github repo for more information.

```sh
git clone https://github.com/LichAmnesia/Robinhood
cd Robinhood
sudo python3 setup.py install
```
