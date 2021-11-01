
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
coin_list = cg.get_coins_list()
coin_list_df = pd.DataFrame(coin_list)

unwanted_ID_list = ['binance-peg-cardano', 'binance-peg-litecoin', 
'binance-peg-avalanche','binance-peg-xrp', 'unicorn-token', 'san-diego-coin',
'hydro-protocol', 'hotnow']

coin_df = coin_list_df[~coin_list_df.id.isin(unwanted_ID_list)]

#get id function

def get_id(symbs):
  stock_id = []
  for s in symbs:
    stock_id.append(coin_df[coin_df.symbol.isin([s])].iloc[0,0])
  return stock_id

#date time format transformation
#from normal time to UNIX format

def timetoUnix(start_date, end_date):
  date_obj_1 = datetime.strptime(start_date, '%m/%d/%y')
  date_obj_2 = datetime.strptime(end_date, '%m/%d/%y')

  range_1 = (date_obj_1 - datetime(1970,1,1)).total_seconds()
  range_2 = (date_obj_2 - datetime(1970,1,1)).total_seconds()
  return range_1, range_2

#we define a function to split list
def slice_per(source, step):
    return [source[i::step] for i in range(step)]

def get_data(symbs, start_date, end_date):
    id_data = get_id(symbs)
    t = timetoUnix(start_date=start_date, end_date=end_date)
    #we get stock data in daily interval
    data = []
    for id in id_data:
        data.append(cg.get_coin_market_chart_range_by_id(id, 'usd', t[0], t[1]))
    #Because we have a nested list of prices, it is necessary flatten it up
    pr={}
    for i in range(0,len(id_data)):
        pr[i] = sum(data[i]['prices'], [])
    #we just need to get prices and dates which they will be stored separately
    prices = []
    dates = []
    for coin in range(0,len(id_data)):
        for price in pr[coin][1::2]:
            prices.append(price)
  
    for date in pr[0][0::2]:
        date = (date/1000)
        e = (datetime.utcfromtimestamp(date).strftime('%m/%d/%y %H:%m'))
        dates.append(e)

        #we need to split data by specific amount of rows (days, minutes, months, etc.)
    partition = int(len(prices) / len(symbs)) + 1
    data_pr = slice_per(prices,partition)
    #converting stock data in dataframe
    pr_df = pd.DataFrame(data_pr, columns=symbs).dropna(axis=0)
    dates_df = pd.DataFrame(dates, columns=['Timestamp']).dropna(axis=0)

    pr_df = pr_df.reset_index(drop=True)
    dates_df = dates_df.reset_index(drop=True)

    df_final = pd.concat([dates_df, pr_df], axis=1).dropna(axis=0)

    return df_final



def plot_stock_data(df):
    df_mean_values = df.mean()
    y1=[]
    y2=[]
    for v in range(len(df_mean_values)):
        if round(df_mean_values[v], 0) >= df_mean_values.mean():
            y1.append(df_mean_values.index[v])
        else:
            y2.append(df_mean_values.index[v])

    ax = df.plot(x='Timestamp', y=y1, figsize=(15,10))
    ax2 = df.plot(x='Timestamp', y=y2,secondary_y=True, ax=ax)
    ax.grid(False, color='k', linestyle='-', linewidth=0.5)
    ax.set_facecolor('1')
    ax.set_ylabel('USD')
    ax2.set_ylabel('USD')
    ax.tick_params(labelsize = 14, axis='x', labelrotation=45)
    ax.tick_params(labelsize = 14)
    ax2.tick_params(labelsize = 14)
    plt.title('Crypto Portfolio graph',fontdict={ 
      'fontsize':22, 
      'fontweight':'bold', 
      'color': 'k'}, loc='center')
    return plt.show()

#df = get_data(['ltc', 'xmr', 'cake', 'uni', 'sol'], '09/15/21','10/09/21')
#plot_stock_data(df)



