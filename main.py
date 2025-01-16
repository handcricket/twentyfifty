from decouple import config
import telepot

import yfinance as yf
import pandas_ta as ta


MY_ID = config("MY_ID")
API_KEY = config("API_KEY")


def check_ema_supertrend(stocks):
    results = []

    data = yf.download(stocks, interval='1h', period='1mo', group_by='ticker')
    
    for stock in stocks:

        stockData = data[stock]
        
        # Calculate EMA(20) and EMA(50)
        stockData['EMA20'] = ta.ema(stockData['Close'], length=20, offset=0)
        stockData['EMA50'] = ta.ema(stockData['Close'], length=50, offset=0)
        
        # Calculate Supertrend (7,3)
        supertrend = ta.supertrend(stockData['High'], stockData['Low'], stockData['Close'], length=10, multiplier=3)

        stockData['Supertrend'] = supertrend['SUPERTd_10_3.0']
    

        # Check for EMA crossover and Supertrend condition
        if stockData['EMA20'].iloc[-1] > stockData['EMA50'].iloc[-1] and stockData['EMA20'].iloc[-2] <= stockData['EMA50'].iloc[-2]:
            if stockData['Supertrend'].iloc[-1] == 1:
                results.append(f"Stock: {stock}, Price: {'{:.2f}'.format(stockData['Close'].iloc[-1])}")
    
    return results



def send_telegram_message(msg):

    bot = telepot.Bot(API_KEY)
    bot.getMe()
    bot.sendMessage(MY_ID, msg)


if __name__ == "__main__":


    stocks = ["BIOCON.NS",
              "BAJFINANCE.NS",
              "BEPL.NS",
              "BHEL.NS",
              "MOREPENLAB.NS",
              "RUPA.NS",
              "GULFOILLUB.NS",
              "GAIL.NS",
              "FORTIS.NS",
              "GHCLTEXTIL.NS",
              "MARKSANS.NS",
              "HPAL.NS",
              "DRREDDY.NS",
              "SUNPHARMA.NS",
              "CIPLA.NS",
              "SUZLON.NS",
              "EPL.NS",
              "CASTROLIND.NS",
              "HSCL.NS",
              "TATACONSUM.NS",
              "AAATECH.NS",
              "NYKAA.NS"]

    crosses = check_ema_supertrend(stocks)

    crossesString =  "\n".join(crosses)

    msg = f"Crosses: \n{crossesString}"

    print(msg)

    if len(crosses) > 0:
        send_telegram_message(msg)