import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def runAnalysis(data: [float]):
    #read in data as an array of arrays of historical values

    #return 0 for no action, 1 for long, 2 for short, 3 for sell?
    df = pd.DataFrame({'Price':data}).tail(30).reset_index(drop=True)
    #get the emas
    df['EMA12'] = df['Price'].ewm(span=12).mean()
    df['EMA26'] = df['Price'].ewm(span=26).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['sigLine'] = df['MACD'].ewm(span=9).mean()

    #check for going long
    last_macd = df['MACD'].iloc[-1]
    last_signal = df['sigLine'].iloc[-1]

    if last_macd > last_signal and last_macd>0:
        return 1
    elif last_macd < last_signal and last_macd<0:
        return -1
    else:
        return 0

    

if __name__ == '__main__':
    df = pd.read_csv('data.csv')
    price_data = df['Price'].tolist()
    indicators = []

    for i in range (30,len(price_data)):
        indicators.append(runAnalysis(price_data[i-30:i]))

    fig,ax = plt.subplots()
    plt.plot(price_data)
    for i,indicator in enumerate(indicators):
        if indicator == 1: #plot the long positions
            plt.scatter(i,price_data[i],marker='x',color='green')

        elif indicator == -1: #plot short positions
            plt.scatter(i,price_data[i],marker='x',color='orange')

        elif indicator==0:#sell position
            plt.scatter(i,price_data[i],marker='x',color='red')


    plt.show()