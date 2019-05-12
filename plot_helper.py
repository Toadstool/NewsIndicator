import share_price as sp
import matplotlib.pyplot as plt
from matplotlib.ticker import Formatter
import numpy as np
from twitter import Twitt 

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
    ax2.scatter(list(map(lambda x: x.date,news)), list(map(lambda x: x.power,news)))
    
    plt.show()    

if __name__ == '__main__':
    import share_price
    from twitt_processing import TwittProcessing

    sharePrice = share_price.getLastWeekIntraday('PKNORLEN','20190512')   
    tw = TwittProcessing()
    data= tw.download('PKNORLEN','20190512')

    plot2(sharePrice,data)