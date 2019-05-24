import requests
import json
import datetime
import time
import os
import matplotlib.pyplot as plt
import jsonpickle

def getLastWeekIntraday(symbol,dateFrom,dateTo):
    df = datetime.datetime.strptime(dateFrom,"%Y%m%d")  
    today = datetime.date.today()    
    if dateTo==None:
        dateTo =today.strftime("%Y%m%d")
    filePath = 'data/LastWeekIntraday_'+symbol+'_'+dateTo +'.json'
    if os.path.isfile(filePath):
        with open(filePath) as json_file:  
            data =  jsonpickle.loads(json_file.read())
            return list(filter(lambda x: x[0]>=df, data))

    print('bankier download itraday')  
    url = 'https://www.bankier.pl/new-charts/get-data?symbol='+symbol+'&intraday=true&type=area'
    resp = requests.get(url)    
    y = json.loads(resp.text)
    items =  y['main']    
    data =  list(map(lambda x: [datetime.datetime.fromtimestamp(int(x[0])/1000), x[1] ], items))
    with open(filePath, 'w+') as outfile: 
        outfile.write(jsonpickle.dumps(data))
    return list(filter(lambda x: x[0]>=df, data))

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
    
    data = getLastWeekIntraday('LPP','20190520','20190525')
    plt.plot(list(map(lambda x: x[0],data)),list(map(lambda x: x[1],data)))
    plt.show()


