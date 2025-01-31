import pandas as pd
import numpy as np
import talib as ta
import yfinance as yf
import matplotlib.pyplot as plt

# Fetch data (example: Nifty 50)
def fetch_data(ticker="^NSEI", period="3mo", interval="60m"):
    data = yf.download(ticker, period=period, interval=interval, group_by='ticker')
    d = data[ticker]
    return d

# Calculate all indicators
def calculate_indicators(df):
    # Trend Indicators
    df['20_EMA'] = ta.EMA(df['Close'], timeperiod=20)
    df['ADX'] = ta.ADX(df['High'], df['Low'], df['Close'], timeperiod=14)
    
    # Momentum Indicators
    df['RSI'] = ta.RSI(df['Close'], timeperiod=14)
    df['MACD'], df['MACD_signal'], _ = ta.MACD(df['Close'])
    
    # Volatility Indicators
    df['ATR'] = ta.ATR(df['High'], df['Low'], df['Close'], timeperiod=14)
    df['upper_band'], df['middle_band'], df['lower_band'] = ta.BBANDS(df['Close'], timeperiod=20)
    
    # Fibonacci Levels (for last 5 days)
    df['fib_38.2'] = df['Close'].rolling(window=5).apply(lambda x: x.max() - (0.382 * (x.max() - x.min())))
    df['fib_50'] = df['Close'].rolling(window=5).apply(lambda x: x.max() - (0.5 * (x.max() - x.min())))
    
    return df

# Generate trading signals
def generate_signals(df):
    df['signal'] = 0  # 1 = Buy, -1 = Sell
    
    # Trend Filter
    uptrend = df['Close'] > df['20_EMA']
    downtrend = df['Close'] < df['20_EMA']
    strong_trend = df['ADX'] > 25
    
    # Pullback Entry Conditions
    pullback_long = (df['Low'] <= df['fib_38.2']) | (df['Low'] <= df['fib_50'])
    rsi_condition = (df['RSI'] >= 40) & (df['RSI'] <= 50)
    volume_condition = df['Volume'] > df['Volume'].rolling(20).mean()
    
    # Breakout Entry Conditions
    breakout = df['Close'] > df['upper_band'].shift(1)
    
    # Generate Signals
    df.loc[uptrend & strong_trend & pullback_long & rsi_condition & volume_condition, 'signal'] = 1
    df.loc[downtrend & breakout, 'signal'] = -1
    
    return df

# Risk Management
def calculate_position_size(df, risk_per_trade=0.01, account_size=100000):
    df['stop_loss'] = df['Low'].rolling(5).min() if df['signal'] == 1 else df['High'].rolling(5).max()
    df['position_size'] = (account_size * risk_per_trade) / (df['Close'] - df['stop_loss'])
    return df

# Backtest
def backtest_strategy(df):
    df['returns'] = df['Close'].pct_change()
    df['strategy_returns'] = df['signal'].shift(1) * df['returns']
    df['cumulative_returns'] = (1 + df['strategy_returns']).cumprod()
    return df

# Main Execution
if __name__ == "__main__":
    # Configuration
    ticker = "^NSEI"  # Nifty 50 example
    account_size = 100000  # INR
    
    # Get Data
    data = fetch_data(ticker)
    
    # Calculate Indicators
    data = calculate_indicators(data)
    
    # Generate Signals
    data = generate_signals(data)
    
    # Risk Management
    data = calculate_position_size(data, account_size=account_size)
    
    # Backtest
    data = backtest_strategy(data)
    
    # Plot Results
    plt.figure(figsize=(15,7))
    plt.plot(data['cumulative_returns'], label='Strategy Returns')
    plt.title('Swing Trading Strategy Performance')
    plt.legend()
    plt.show()

    # Print Key Metrics
    print(f"Total Returns: {data['cumulative_returns'][-1]*100:.2f}%")
    print(f"Number of Trades: {len(data[data['signal'] != 0])}")