import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
data = yf.download(tickers='PLTR', start="2025-06-01", end="2026-07-21")
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

data['SMA_Short'] = data['Close'].rolling(window = 20).mean()
data['SMA_Long'] = data['Close'].rolling(window = 50).mean()
print(data.head(30))