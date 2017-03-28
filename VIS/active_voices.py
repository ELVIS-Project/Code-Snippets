'''function that reads in series of "active voices result" (y) and manipulates
numerosity to be more stable over time by manipulating window size (win).
Sets the minimum number of voices in the texture to "min".'''

def voicefilter(y, win, min):

    import pandas as pd

    av_col = y.copy()
    x = av_col['active_voices.ActiveVoicesIndexer', 'Active Voices']

    if(x.iloc[0] < min):
        x.iloc[0] = min
    for i in range(1, len(x)):
        if(x.iloc[i] < min):
            x.iloc[i] = min
        if(x.iloc[i] < x.iloc[i-1]):
            if(x.iloc[i] < x.iloc[i+1]):
                x.iloc[i] = max(x.iloc[i-1], x.iloc[i+1])
            elif(any([j > x.iloc[i] for j in x.iloc[i+1:i+win]])):
                x.iloc[i] = max(x.iloc[i+1:i+win])
    return(pd.Series(data = x, index = av_col.index))