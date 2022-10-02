from markdown import markdownFromFile
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf # candlestick_ohlc
import requests
from datetime import datetime
import time

bougth_price = 120.0

# Get the data from the API
symbol = 'IBM' # IBM stock symbol
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + symbol + '&interval=5min&apikey=demo'
r = requests.get(url)
data = r.json()


# Metadata
last_refreshed = data['Meta Data']['3. Last Refreshed']
symbol = data['Meta Data']['2. Symbol']
tymezone = data['Meta Data']['6. Time Zone']


# Process the data
date, openp, highp, lowp, closep, volume = [], [], [], [], [], []

for key, value in data['Time Series (5min)'].items():
    open_price, highp_price, low_price, close_price, volume_item = value.values()
    date.append(datetime.strptime(key, '%Y-%m-%d %H:%M:%S'))
    openp.append(float(open_price))
    highp.append(float(highp_price))
    lowp.append(float(low_price))
    closep.append(float(close_price))
    volume.append(float(volume_item))

date = np.array(date, dtype='datetime64[m]')    
openp = np.array(openp, dtype=np.float64)
highp = np.array(highp, dtype=np.float64)
lowp = np.array(lowp, dtype=np.float64)
closep = np.array(closep, dtype=np.float64)
volume = np.array(volume, dtype=np.float64)

# Plot the data

# Group the data in tuples to use with candlestick module
ohlc = np.array([[date[i], openp[i], highp[i], lowp[i], closep[i], volume[i]] for i in range(len(date))])

# Transform ohlc to a DataFrame to use with mplfinance
ohlc_df = pd.DataFrame(ohlc, columns=['time_period_start', 'Open', 'High', 'Low', 'Close', 'Volume'])

# transform the date to a datetime object
ohlc_df.time_period_start = pd.to_datetime(ohlc_df.time_period_start)

# Set date as index
ohlc_df = ohlc_df.set_index('time_period_start')

# Sort index in ascending order
ohlc_df = ohlc_df.sort_index(ascending=True)

ohlc_df = ohlc_df.astype(float)


mpf.plot(ohlc_df, type='candle', style='yahoo', title='{} Stock Price'.format(symbol), ylabel='Price ($)', ylabel_lower='Volume', volume=True, mav=(3,6,9), figratio=(10,8), figscale=0.8)





