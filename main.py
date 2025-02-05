from decouple import config
import telepot

import yfinance as yf
import pandas_ta as ta


MY_ID = config("MY_ID")
API_KEY = config("API_KEY")


def send_telegram_message(msg):

    bot = telepot.Bot(API_KEY)
    bot.getMe()
    bot.sendMessage(MY_ID, msg)


def volatility_adaptive_trailer(stockData, mult=5, slope_input=50):

    df = stockData.copy()
    
    # Calculate parameters
    slope = slope_input * mult
    
    # Calculate ATR and adjust
    df['atr'] = ta.atr( df['High'], df['Low'], df['Close'], length=200)
    df['atr'] = df['atr'].fillna(0.0)
    df['adjusted_atr'] = df['atr'] * mult
    
    # Initialize arrays
    pc_avg = [0.0] * len(df)
    hold_atr = [0.0] * len(df)
    os = [1] * len(df)
    
    # Initial values
    pc_avg[0] = df['Close'].iloc[0]
    
    # Main calculation loop
    for i in range(1, len(df)):
        current_close = df['Close'].iloc[i]
        prev_pc_avg = pc_avg[i-1]
        current_atr = df['adjusted_atr'].iloc[i]
        
        # Calculate pc_avg and hold_atr
        if abs(current_close - prev_pc_avg) > current_atr:
            pc_avg[i] = current_close
            hold_atr[i] = current_atr / 2
        else:
            pc_avg[i] = prev_pc_avg + (os[i-1] * hold_atr[i-1]) / slope
            hold_atr[i] = hold_atr[i-1]
        
        # Determine os value
        if pc_avg[i] > prev_pc_avg:
            os[i] = 1
        elif pc_avg[i] < prev_pc_avg:
            os[i] = -1
        else:
            os[i] = os[i-1]
    
    # Add results to DataFrame
    df['pc_avg'] = pc_avg
    df['hold_atr'] = hold_atr
    df['os'] = os
    df['pc_S2'] = df['pc_avg'] - df['hold_atr']

    if (df['Close'].iloc[-1] == df['pc_S2'].iloc[-1]):
        return 0
    return (df['pc_S2'].iloc[-1])

def check_trend(stocks):
    results = []
    
    for stock in stocks:

        try:

            data = yf.download([stock], interval='1d', period='max', group_by='ticker')

            stockData = data[stock].copy()

            pc_s2 = volatility_adaptive_trailer(stockData)

            stockData['pc_s2'] = pc_s2

            # check price crossover pc_s2
            # if the signals are less, the use the below code => this will consider only latest pc_s2
            # if (stockData['Close'].iloc[-2] < stockData['pc_s2'].iloc[-1]) and (stockData['Close'].iloc[-1] > stockData['pc_s2'].iloc[-1]):
            #     results.append(f"Stock: {stock}, Price: {'{:.2f}'.format(stockData['Close'].iloc[-1])}")

            # check price crossover pc_s2
            # if (stockData['Close'].iloc[-2] < stockData['pc_s2'].iloc[-2]) and (stockData['Close'].iloc[-1] > stockData['pc_s2'].iloc[-1]):
            #     results.append(f"Stock: {stock}, Price: {'{:.2f}'.format(stockData['Close'].iloc[-1])}")

            # check price crossover pc_s2
            if (stockData['Low'].iloc[-1] < stockData['pc_s2'].iloc[-1]) and (stockData['Close'].iloc[-1] > stockData['pc_s2'].iloc[-1]):
                results.append(f"Stock: {stock}, Price: {'{:.2f}'.format(stockData['Close'].iloc[-1])}")

        except Exception as e:
            print(f"Error: {e}")
    
    return results



if __name__ == "__main__":


    stocks = [
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
              "TATACONSUM.NS",
              "AAATECH.NS",
              "SIEMENS.NS",
              "ASIANPAINT.NS",
              "NESTLEIND.NS",
              "TRENT.NS",
              "ULTRACEMCO.NS",
              "HINDUNILVR.NS",
              "APOLLOHOSP.NS",
              "BRITANNIA.NS",
              "VOLTAS.NS",
              "LLOYDSENGG.NS"
              ]

    crosses = check_trend(stocks)

    crossesString =  "\n".join(crosses)

    msg = f"Crosses: \n{crossesString}"

    print(msg)

    if len(crosses) > 0:
        send_telegram_message(msg)

