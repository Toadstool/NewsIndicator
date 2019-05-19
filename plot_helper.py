import share_price as sp
import matplotlib.pyplot as plt
from matplotlib.ticker import Formatter
import numpy as np
from twitter import Twitt 
from functools import reduce
import datetime

class DateFormatter(Formatter):
    def __init__(self, dates, fmt='%Y-%m-%d'):
        self.dates = dates
        self.fmt = fmt

    def __call__(self, x, pos=0):
        
        ind = int(np.round(x))
        if ind >= len(self.dates) or ind < 0:
            return ''
        return self.dates[ind].strftime(self.fmt)

  
def plot(data) :   
    formatter = DateFormatter(list(map(lambda x: x[0],data)))
    plt.rcParams['figure.figsize'] = [15, 5]
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(formatter)
    ax.plot(np.arange(len(data)), list(map(lambda x: x[1],data)))
    fig.autofmt_xdate()
    plt.show()    

def plot2(sharePrice,news) :
    
    plt.rcParams['figure.figsize'] = [15, 5]   

    ax1 = plt.subplot(311)
    ax2 = plt.subplot(312, sharex=ax1)
    ax1.set_title('share price')
    ax1.plot(list(map(lambda x: x[0],sharePrice)), list(map(lambda x: x[1],sharePrice)))
    ax2.set_title('news power')

    maxdata = reduce(lambda x, y: y[0] if y[0]> x else x ,sharePrice,datetime.datetime.min)
    

    d1 = list(filter(lambda x: x.ignore and x.date < maxdata,news))  
    if len(d1)>0: 
        ax2.scatter(list(map(lambda x: x.date,d1)), 
                list(map(lambda x: x.power,d1)),
                s = list(map(lambda x: ((abs(x.sentiment)+1)*5)**2,d1)),
                marker= 'o',
                c='blue')

    d2 = list(filter(lambda x: not x.ignore and x.sentiment==0 and x.date < maxdata,news))    
    if len(d2)>0: 
        ax2.scatter(list(map(lambda x: x.date,d2)), 
                list(map(lambda x: x.power,d2)),
                s = list(map(lambda x: ((abs(x.sentiment)+1)*5)**2,d2)),
                marker= 's',
                c='yellow')                

    d3 = list(filter(lambda x: not x.ignore and x.sentiment>0 and x.date < maxdata,news))   
    if len(d3)>0:
        ax2.scatter(list(map(lambda x: x.date,d3)), 
                list(map(lambda x: x.power,d3)),
                s = list(map(lambda x: ((abs(x.sentiment)+1)*5)**2,d3)),
                marker= '^',
                c='green')
    d4 = list(filter(lambda x: not x.ignore and x.sentiment<0 and x.date < maxdata,news))    
    if len(d4)>0:
        ax2.scatter(list(map(lambda x: x.date,d4)), 
                list(map(lambda x: x.power,d4)),
                s = list(map(lambda x: ((abs(x.sentiment)+1)*5)**2,d4)),
                marker= 'v',
                c='red')





    
    plt.show()    

if __name__ == '__main__':
    import share_price
    from twitt_processing import TwittProcessing

    sharePrice = share_price.getLastWeekIntraday('PKNORLEN','20190512')   
    tw = TwittProcessing()
    data= tw.download('PKNORLEN','20190512')

    plot2(sharePrice,data)