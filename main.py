from decouple import config
import telepot

import pandas as pd
import yfinance as yf
import ta


MY_ID = config("MY_ID")
API_KEY = config("API_KEY")


def check_ema_supertrend(stocks):
    results = []
    
    for stock in stocks:
        # Fetch 1-hour historical data for the last 2 days to ensure enough data points
        data = yf.download(stock, interval='1h', period='2d')
        
        if len(data) < 50:
            continue  # Skip if not enough data
        
        # Calculate EMA(20) and EMA(50)
        data['EMA20'] = ta.trend.ema_indicator(data['Close'], window=20)
        data['EMA50'] = ta.trend.ema_indicator(data['Close'], window=50)
        
        # Calculate Supertrend (7,3)
        supertrend = ta.trend.supertrend(data['High'], data['Low'], data['Close'], length=7, multiplier=3)
        data['Supertrend'] = supertrend['supertrend']
        
        # Check for EMA crossover and Supertrend condition
        if data['EMA20'].iloc[-1] > data['EMA50'].iloc[-1] and data['EMA20'].iloc[-2] <= data['EMA50'].iloc[-2]:
            if data['Supertrend'].iloc[-1] < data['Close'].iloc[-1]:
                results.append(stock)
    
    return results

def getSpecials():

    return 'cleanest_specials'


def send_telegram_message(msg):

    bot = telepot.Bot(API_KEY)
    bot.getMe()
    bot.sendMessage(MY_ID, msg)


if __name__ == "__main__":

    # Get the specials
    meats = getSpecials()

    stocks = ["BIOCON.NS", "BAJFINANCE.NS"]

    crosses = check_ema_supertrend(stocks)

    stocksString =  "\n".join(stocks)
    crossesString =  "\n".join(crosses)

    msg = f"Specials: \n{crossesString} \n\nMeats: \n{meats} \n\nStocks: \n{stocksString}"

    send_telegram_message(msg)