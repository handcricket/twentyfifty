from decouple import config
import telepot

import yfinance as yf
import pandas_ta as ta


MY_ID = config("MY_ID")
API_KEY = config("API_KEY")


def check_ema_supertrend(stocks):
    results = []
    
    for stock in stocks:
        # Fetch 1-hour historical data for the last 5 days to ensure enough data points
        data = yf.download(stock, interval='1h', period='1mo', group_by='ticker')

        stockData = data[stock]
        
        # Calculate EMA(20) and EMA(50)
        stockData['EMA20'] = ta.ema(stockData['Close'], length=20, offset=0)
        stockData['EMA50'] = ta.ema(stockData['Close'], length=50, offset=0)
        
        # Calculate Supertrend (7,3)
        supertrend = ta.supertrend(stockData['High'], stockData['Low'], stockData['Close'], length=10, multiplier=3)

        stockData['Supertrend'] = supertrend['SUPERTd_10_3.0']

        print(stockData)
        
        # Check for EMA crossover and Supertrend condition
        if stockData['EMA20'].iloc[-1] > stockData['EMA50'].iloc[-1] and stockData['EMA20'].iloc[-2] <= stockData['EMA50'].iloc[-2]:
            if stockData['Supertrend'].iloc[-1] == 1:
                results.append(stock)
    
    return results



def send_telegram_message(msg):

    bot = telepot.Bot(API_KEY)
    bot.getMe()
    bot.sendMessage(MY_ID, msg)


if __name__ == "__main__":

    stocks = ["BIOCON.NS", "BAJFINANCE.NS"]

    crosses = check_ema_supertrend(stocks)

    crossesString =  "\n".join(crosses)
    stocksString =  "\n".join(stocks)

    msg = f"Crosses: \n{crossesString} on {stocksString}"

    print(msg)

    # if len(crosses) > 0:
    #     send_telegram_message(msg)

    send_telegram_message(msg)