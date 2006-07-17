import MySQLdb
import datetime
from ta.Sma import Sma
from ta.TimeFrame import TimeFrame

class TAdb:
    def __init__(self, host='',user='', pwd=''):
        if not host: self.host = '10.0.0.152'
        else: self.host = host
        self.port = 3306
        self.dbase   = 'ta'
        if not user: self.user = 'py3'; self.pwd = 'py3'
        else: self.user = user; self.pwd = pwd
        self.db = MySQLdb.connect(host=self.host, port = self.port, user = self.user, passwd = self.pwd, db = self.dbase)
 
    def cursor(self, *args, **kwargs):
        return self.db.cursor(*args, **kwargs)
     
    def execute(self, string):
        cur = self.db.cursor()
        cur.execute(string)
        list = []
        try:
            for x in cur.fetchall():
                list.append(x)
        except:
            list = None
        return list
    
    def exampleTickData(self):
        
        sql = "SELECT date, time, open, high, low, close FROM candlesticks WHERE ticker_id=102 AND period=1 order by date, time limit 600"
        data = self.execute(sql)
    
        result = []
        for candle in data:
            d = datetime.datetime(candle[0].year, candle[0].month, candle[0].day) + candle[1]
            d = d - datetime.timedelta(0, 60) # correct for database storage
 
            for i in range(4):
                tick = (d, candle[i+2])
                result.append((tick[0], tick[1]))
                d = d + datetime.timedelta(0, 15)
        return result
            
if __name__ == '__main__':
    
    ta = TAdb()
    
    s = Sma(12)
    tf = TimeFrame(17, indicators=[s])
    
    sql = "SELECT date, time, open, high, low, close FROM candlesticks WHERE ticker_id=102 AND period=1 order by date, time limit 600"
    data = ta.execute(sql)
    
    print "fetched candles"
    
    for candle in data:
        d = datetime.datetime(candle[0].year, candle[0].month, candle[0].day) + candle[1]
        d = d - datetime.timedelta(0, 60) # correct for database storage
        # print d
        for i in range(4):
            tick = (d, candle[i+2])
            tf.handleTick(tick[0], tick[1])
            d = d + datetime.timedelta(0, 15)
            
    print tf.times
    print tf.indicators[0].output
    
    
