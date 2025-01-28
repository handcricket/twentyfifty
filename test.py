import yfinance as yf
import pandas_ta as ta

def calculate_predictive_channels(df, factor=5, slope_input=50):
    """
    Calculate Predictive Channels for a given DataFrame containing OHLC data.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing columns 'high', 'low', 'close'
    factor (float): Multiplier for ATR (default: 5)
    slope_input (float): Slope input value (default: 50)
    
    Returns:
    pd.DataFrame: Original DataFrame with added columns for predictive channels
    """
    df = df.copy()
    # Calculate parameters
    mult = factor
    slope = slope_input * mult  # Total slope value
    
    # Calculate ATR(200) and multiply by factor
    df['atr'] = ta.atr(df['High'], df['Low'], df['Close'], length=200)
    # df['atr'] = df['atr'].fillna(0) * mult  # Handle NaN values and apply multiplier
    
    # # Initialize columns
    # df['pc_avg'] = pd.Series(dtype=float)
    # df['hold_atr'] = 0.0
    # df['os'] = 1
    
    # # Initialize first values
    # df.loc[0, 'pc_avg'] = df.loc[0, 'Close']
    # df.loc[0, 'hold_atr'] = 0.0
    # df.loc[0, 'os'] = 1
    
    # # Iterate through DataFrame to calculate values
    # for i in range(1, len(df)):
    #     prev_pc_avg = df.loc[i-1, 'pc_avg']
    #     current_close = df.loc[i, 'Close']
    #     current_atr = df.loc[i, 'atr']
    #     prev_hold_atr = df.loc[i-1, 'hold_atr']
    #     prev_os = df.loc[i-1, 'os']
        
    #     # Calculate current pc_avg and hold_atr
    #     if abs(current_close - prev_pc_avg) > current_atr:
    #         current_pc_avg = current_close
    #         current_hold_atr = current_atr / 2
    #     else:
    #         current_pc_avg = prev_pc_avg + (prev_os * prev_hold_atr) / slope
    #         current_hold_atr = prev_hold_atr
        
    #     # Determine current OS value
    #     if current_pc_avg > prev_pc_avg:
    #         current_os = 1
    #     elif current_pc_avg < prev_pc_avg:
    #         current_os = -1
    #     else:
    #         current_os = prev_os
        
    #     # Update current values
    #     df.loc[i, 'pc_avg'] = current_pc_avg
    #     df.loc[i, 'hold_atr'] = current_hold_atr
    #     df.loc[i, 'os'] = current_os
    
    # # Calculate channel values
    # df['pc_R2'] = df['pc_avg'] + df['hold_atr']
    # df['pc_R1'] = df['pc_avg'] + df['hold_atr'] / 2
    # df['pc_S1'] = df['pc_avg'] - df['hold_atr'] / 2
    # df['pc_S2'] = df['pc_avg'] - df['hold_atr']
    print(df)
    return df

# Example usage:
# Assuming you have a DataFrame 'ohlc_data' with 'high', 'low', 'close' columns
# ohlc_data = pd.read_csv('your_data.csv')

data = yf.download("BEPL.NS", interval='1d', period='max', group_by='ticker')
ohlc_data = data['BEPL.NS'].copy()
result_df = calculate_predictive_channels(ohlc_data)
# print(result_df[['close', 'pc_avg', 'pc_R2', 'pc_R1', 'pc_S1', 'pc_S2']].tail())