from smartapi.smartConnect import SmartConnect
import pandas as pd
from datetime import datetime, date, time, timedelta
import requests
import numpy as np
from smartapi import SmartWebSocket
import time as tt
from talib.abstract import *
 

#anngel one api id and password
apikey='*******'
username= "******"
pwd= '*******'

#telegram bot 
BOT_TOKEN='**************'
BOT_CHAT_ID='*********'

#connecting with anngel one api
def login():
    obj=SmartConnect(api_key=apikey)
    data = obj.generateSession(username,pwd)
    refreshToken= data['data']['refreshToken']
    res= obj.getProfile(refreshToken)
    res['data']['exchanges']
    return obj

#extracting token details
def getSymbolToken():
    url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
    d = requests.get(url).json()
    token_df = pd.DataFrame.from_dict(d)
    token_df['expiry'] = pd.to_datetime(token_df['expiry'])
    token_df = token_df.astype({'strike':float})
    return token_df

#getting candle data for each token
def getCandleData(token):
    
    try:
        historicParam={
        "exchange": "NSE",
        "symboltoken": token,
        "interval": "ONE_DAY",
        "fromdate": f'{date.today()- timedelta (days=60)} 09:15',
        "todate": f'{date.today()} 09:15'
        }
        return obj.getCandleData(historicParam)
    except Exception as e:
        print(f"Historic Api failed: {e.message}")    

#specifying condition for filtering the stock
def scanStocks():
    lookbackDay = 5
    start = tt.time()
    highList = []
    lowList =[]
    angel_obj = login()
    token_df = getSymbolToken()
    symbol_token = token_df[(token_df.exch_seg=='NFO') & (token_df.instrumenttype=='FUTSTK')]
    fnoSymbol=symbol_token['name'].unique()
    symbolDf=token_df[token_df.symbol.str.endswith('-EQ') & (token_df.exch_seg=='NSE') & token_df.name.isin(fnoSymbol)].sort_values(by= 'symbol')
    symbolDf.reset_index(inplace=True) 
    symbolDf
    for i in symbolDf.index:
        try:
            symbol = symbolDf.loc[i]['symbol']
            token = symbolDf.loc[i]['token']
            res = getCandleData(token)
            candleInfo = pd.DataFrame(res['data'],columns = ['data', 'open', 'high', 'low', 'close', 'vol'])
            candleInfo['RSI'] = RSI(candleInfo.close, timeperiod = 14)
            recentCandle = candleInfo.iloc[-1] 

            lastndaysCandle = candleInfo.iloc[-(lookbackDay+1):-1]
            Avol = candleInfo.iloc[-21:-1].vol.mean()
            high = lastndaysCandle.high.max()
            low = lastndaysCandle.low.min()
            
            if recentCandle.close > high and recentCandle.RSI >= 60 and recentCandle.vol >= Avol:
                #print('High break', high ,recentCandle.close, symbol)
                highList .append (symbol)
        
            elif recentCandle.close < low and recentCandle.RSI <= 40 and recentCandle.vol >= Avol:
                #print ('Low break', low ,recentCandle.close, symbol)
                lowList.append (symbol)
                
            tt.sleep(0.1)
        except Exception as e:
            print( "Error in scan for " ,symbol, e )

#creating a connection with telegram bot
def telegram_bot_sendtext(bot_message) :

    send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + BOT_CHAT_ID +                 '&parse_mode=HTML&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

#sending the list of low breakouts
def divide_chunks(l, n):
    for i in range(0, len(l), n): 
        yield l[i:i + n]
n = 30
l = list(divide_chunks(lowList, n))
telegram_bot_sendtext(f'Low Breakout:')
for i in l:
    telegram_bot_sendtext(str(i))
if len(l) == 0:
    telegram_bot_sendtext(f'No Stock')

#sending the list of high breakouts
h = list(divide_chunks(highList, n))
telegram_bot_sendtext(f'High Breakout:')
for e in h:
    telegram_bot_sendtext(str(e))
if len(h) == 0:
    telegram_bot_sendtext(f'No Stock')



