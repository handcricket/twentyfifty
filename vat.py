import pandas_ta as ta
class vat:
    def __init__(self, stockData, mult=5, slope_input=50):
        self.stockData =  stockData
        self.mult = mult
        self.slope_input = slope_input

    def volatility_adaptive_trailer(self):
        df = self.stockData.copy()
    
        # Calculate parameters
        slope = self.slope_input * self.mult
        
        # Calculate ATR and adjust
        df['atr'] = ta.atr( df['High'], df['Low'], df['Close'], length=200)
        df['atr'] = df['atr'].fillna(0.0)
        df['adjusted_atr'] = df['atr'] * self.mult
        
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