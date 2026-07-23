import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
data = yf.download(tickers='PLTR', start="2025-05-01", end="2026-07-21")
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

data['SMA_Short'] = data['Close'].rolling(window = 20).mean()
data['SMA_Long'] = data['Close'].rolling(window = 50).mean()

data['signal'] = (data['SMA_Short']>data['SMA_Long']).astype(int)

buy_signals = data[data['signal'].diff() == 1]
sell_signals = data[data['signal'].diff() == -1]
print(data.head(50))
print('buy signals')
print(buy_signals.head(50))
print('sell signals')
print(sell_signals.head(50))

data['returns'] = data['Close'].pct_change()
data['strategy_returns'] = data['returns'] * data['signal'].shift(1)

data['cumulative_returns'] = (1 + data['strategy_returns']).cumprod()
print("Фінальна дохідність стратегії:", data['cumulative_returns'].iloc[-1])