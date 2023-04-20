import yfinance as yf
import pandas as pd
import pandas_ta as pta
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import pandas_datareader as pdr
from sklearn.metrics import mean_squared_error
from math import sqrt

def col_generator(tick, names, shifts=14, years='5y'):
    stock = yf.Ticker(ticker=tick).history(period=years)
    
    for i in range(0, shifts):
        stock[f'shift_{i+1}'] = stock['Close'].shift(i+1)
        names.append(f'shift_{i+1}')
    
    stock['RSI'] = pta.rsi(stock['Close'], length=14)
    names.append('RSI')
    
    exp1 = stock['Close'].ewm(span=12).mean()
    exp2 = stock['Close'].ewm(span=26).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9).mean()

    stock['macd'] = macd
    # stock['signal'] = signal
    names.append('macd')
    # names.append('signal')
    
    df = stock.copy()
    df.drop(['Open','High','Low', 'Volume', 'Dividends','Stock Splits'], axis=1, inplace=True)
    df.dropna(inplace=True)
    
    return df, names



def setter(tick):
    shifts = [7,14,31]
    years = ['1y', '3y', '5y']
    scores = []
    for j in range(len(shifts)):

        for k in range(len(years)):

            names = []
        
            df, names = col_generator(tick, names, shifts[j], years[k])
            #print(tick[i], shifts[j], years[k])

            train, test = train_test_split(df, shuffle=False, test_size=0.3, random_state=0)

            scaler = StandardScaler()
            scaler = scaler.fit(train[names])
            X_train = scaler.transform(train[names])
            X_test = scaler.transform(test[names])

            scaler1 = StandardScaler().fit(np.array(train['Close']).reshape(-1,1))
            y_train = scaler1.transform(np.array(train['Close']).reshape(-1,1))
            y_test = scaler1.transform(np.array(test['Close']).reshape(-1,1))

            regress = LinearRegression()
            regress.fit(X_train, y_train)
            score = regress.score(X_test, y_test)*100
            #print(score)

            inverse_pred = scaler1.inverse_transform(regress.predict(X_test))

            inverse_true = scaler1.inverse_transform(y_test)

            MSE_LR = sqrt(mean_squared_error(y_true=inverse_true, y_pred=inverse_pred))

            #print(f'Root Mean Squared Error: {MSE_LR}')
            scores.append({'ticker':tick, 'shifts': shifts[j], 'years':years[k],'accuracy': score, 'rmse': MSE_LR})
            #print('------------------------------------')

            names = names.clear()
            del df, train, test, scaler, X_test, X_train, scaler1, y_train, y_test, regress, score


    scores_df = pd.DataFrame(scores)
    # sort the DataFrame by accuracy (descending) and then by RMSE (ascending)
    scores_df = scores_df.sort_values(by=['rmse','accuracy'], ascending=[True, False])
    #print(scores_df)
    # select the scenario with the highest accuracy score and lowest RMSE score
    best_scenario = scores_df.iloc[0]
    #print(best_scenario)
    #print(best_scenario['shifts'], best_scenario['years'])
    return best_scenario['shifts'], best_scenario['years']
    
#print(scores_df)
#tick = ['RELIANCE.NS','TCS.NS']
#setter(tick[1])