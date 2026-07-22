import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
data = yf.download(tickers='PLTR', start="2025-06-01", end="2026-07-21")
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)
print(data.head())