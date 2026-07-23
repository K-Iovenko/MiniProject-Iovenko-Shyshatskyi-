import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
data = yf.download(tickers='PLTR', start="2025-06-01", end="2026-07-21")
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

data['SMA_Short'] = data['Close'].rolling(window = 20).mean()
data['SMA_Long'] = data['Close'].rolling(window = 50).mean()

data['signal'] = (data['SMA_Short']>data['SMA_Long']).astype(int)

buy_signals = data[data['signal'].diff() == 1]
sell_signals = data[data['signal'].diff() == -1]


data['returns'] = data['Close'].pct_change()
data['strategy_returns'] = data['returns'] * data['signal'].shift(1)

data['cumulative_returns'] = (1 + data['strategy_returns']).cumprod()
data['buy_hold_returns'] = (1 + data['returns']).cumprod()

total_return_strategy = data['cumulative_returns'].iloc[-1] - 1
total_return_bh = data['buy_hold_returns'].iloc[-1] - 1
num_trades = len(buy_signals) + len(sell_signals)

print(f"Дохідність стратегії: {total_return_strategy:.2%}")
print(f"Дохідність Buy&Hold: {total_return_bh:.2%}")
print(f"Кількість угод: {num_trades}")


plt.figure(figsize=(14, 7))
plt.plot(data.index, data['Close'], label='Ціна закриття', alpha=0.6)
plt.plot(data.index, data['SMA_Short'], label='SMA 20', alpha=0.8)
plt.plot(data.index, data['SMA_Long'], label='SMA 50', alpha=0.8)
plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', label='Купівля', s=100)
plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', label='Продаж', s=100)
plt.title('Moving Average Crossover Strategy — PLTR')
plt.xlabel('Дата')
plt.ylabel('Ціна')
plt.legend()
plt.show()