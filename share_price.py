import requests
import json
import datetime
import time
import matplotlib.pyplot as plt

def getLastWeekIntraday(symbol):
    url = 'https://www.bankier.pl/new-charts/get-data?symbol='+symbol+'&intraday=true&type=area'
    resp = requests.get(url)    
    y = json.loads(resp.text)
    items =  y['main']    
    return list(map(lambda x: [datetime.datetime.fromtimestamp(int(x[0])/1000), x[1] ], items))

def getLastIntraday(symbol,days):

    date_from = int(time.mktime((datetime.datetime.now() - datetime.timedelta(days=days)).timetuple())* 1000)
    date_to = int(time.mktime(datetime.datetime.now().timetuple())* 1000)
    url = 'https://www.bankier.pl/new-charts/get-data?date_from='+str(date_from)+'&date_to='+str(date_to)+'&symbol='+symbol+'&intraday=true&type=area'
    resp = requests.get(url)    
    y = json.loads(resp.text)
    items =  y['main']    
    return list(map(lambda x: [datetime.datetime.fromtimestamp(int(x[0])/1000), x[1] ], items))

def getLastDays(symbol,days):

    date_from = int(time.mktime((datetime.datetime.now() - datetime.timedelta(days=days)).timetuple())* 1000)
    date_to = int(time.mktime(datetime.datetime.now().timetuple())* 1000)
    url = 'https://www.bankier.pl/new-charts/get-data?date_from='+str(date_from)+'&date_to='+str(date_to)+'&symbol='+symbol+'&intraday=false&type=area'
    resp = requests.get(url)    
    y = json.loads(resp.text)
    items =  y['main']    
    return list(map(lambda x: [datetime.datetime.fromtimestamp(int(x[0])/1000), x[1] ], items))

if __name__ == '__main__':
    
    data = getLastDays(20,'PKOBP')
    plt.plot(list(map(lambda x: x[0],data)),list(map(lambda x: x[1],data)))
    plt.show()


