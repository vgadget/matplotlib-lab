from markdown import markdownFromFile
import numpy as np
import matplotlib.pyplot as plt
import requests

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
from datetime import datetime

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
openp = np.array(openp, dtype=np.float)
highp = np.array(highp, dtype=np.float)
lowp = np.array(lowp, dtype=np.float)
closep = np.array(closep, dtype=np.float)
volume = np.array(volume, dtype=np.float)



# Plot the data
plt.rcParams["axes.labelweight"] = "bold" # Make the axis labels bold
fig = plt.figure(figsize=(20, 5))

# Rotate the x-axis labels
ax = plt.subplot2grid((1, 1), (0, 0))
for label in ax.xaxis.get_ticklabels():
    label.set_rotation(45)
    
ax.xaxis.label.set_color('navy')
ax.yaxis.label.set_color('black')

ax.grid(True, color='grey', linestyle='-', linewidth=0.25, alpha=0.5)

ax.plot_date(date, closep, linestyle='solid', color='orange', label='Close Price', linewidth=0.8, alpha=0.8, marker='o', markersize=2)

# Fill with green the area between where the price is higher than the bought price
ax.fill_between(date, closep, bougth_price, where=(closep > bougth_price), facecolor='green', alpha=0.5)
# Fill with red the area between where the price is lower than the bought price
ax.fill_between(date, closep, bougth_price, where=(closep < bougth_price), facecolor='red', alpha=0.5)

# Add horizontal line at the bought price
ax.axhline(y=bougth_price, color='blue', linestyle='--', linewidth=1)

# Fake plot to create the color legend
ax.plot([], [], linewidth=5, color='green', label='Profit', alpha=0.5)
ax.plot([], [], linewidth=5, color='red', label='Loss', alpha=0.5)
ax.plot([], [], linewidth=1, color='blue', label='Bought Price', linestyle='--')


# Adjust the plot
plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)

plt.suptitle('Stock price of ' + symbol + ' over time')
plt.title('Last refreshed: ' + last_refreshed + ' ' + tymezone, fontsize=10)
plt.xlabel('Date')
plt.ylabel('Price')

plt.legend()
plt.show()