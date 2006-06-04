import logging
import logging.config
import os
import datetime
from CandleGenerator import CandleGenerator
from Sma import Sma

class TimeFrame:
    
    def __init__(self, period, *args, **kwargs):
        
        self.period = period
        self.indicators = []
        
        self.candleGenerator = CandleGenerator(period)
        
        self.times = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
        
        self.logger = logging.getLogger(self.__class__.__name__)
        try: logging.config.fileConfig(os.getcwd() + "/logging.conf")
        except: logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', filename=self.__class__.__name__+'.log', filemode='w')
        
        if kwargs.has_key('indicators'):
            if not type(kwargs['indicators']) is list:
                self.logger.debug(self + "; indicators passed via keywords is not a list as required.")
            else: self.indicators = kwargs['indicators']
        
    def append(self, value):
        # check if valid input
        if not self._validate(value): return False
        self.virtualCheck(value)
        self.updateLists(value)
        for ind in self.indicators:
            ind.append(value)
        
    def handleTick(self, time, last):
        if not self._validateTick(time, last):
            # raise Error
            return
        candles = self.candleGenerator.processTick(time, last)
        if candles:
            for candle in candles:
                self.append(candle)
        
    def _validate(self, value):
        if type(value) is tuple:
            if len(value) != 6:
                self.logger.error('invalid input: tuple length should be 6; input: %s' % (value,)) 
                return False
            elif not type(value[0]) is datetime.datetime:
                self.logger.error('invalid input: tuple element [0] should be a datetime; input: %s' % (value[0],)) 
                return False
            else:
                for i in range(1,6):
                    if type(value[i]) is int or type(value[i]) is float: continue
                    else:
                        self.logger.error('invalid input: tuple element [%s] is not int or float; input: %s' % (i,value[i])) 
                        return False
            if len(self.times) > 0 and value[0] < self.times[-1]:
                self.logger.error('invalid input: tuple element [0] (datetime) should be greater than previous: %s; input: %s' % (self.times[-1]), value[0]) 
                return False
            return True
        else:
            self.logger.error('invalid input: should be a tuple (d, o, h, l, c, v); input: %s' % (value,)) 
            return False
        
    def _validateTick(self, time, last):
        if not time:
            self.logger.error('invalid input: time is not supplied') 
            return False
        if not last:
            self.logger.error('invalid input: last is not supplied') 
            return False
        if not type(time) is datetime.datetime:
            self.logger.error('invalid input: time should be a datetime; input: %s' % (time,)) 
            return False
        if not (type(last) is int or type(last) is float):
            self.logger.error('invalid input: last should be an int or float; input: %s' % (last,)) 
            return False    
        return True
        
    def virtualCheck(self, value):
        if len(self.times) > 0 and self.times[-1] == value[0]:
            # now revert back to previous state, remove previous virtual candle
            self.times = self.times[:-1]
            self.opens = self.opens[:-1]
            self.highs = self.highs[:-1]
            self.lows = self.lows[:-1]
            self.closes = self.closes[:-1]
            self.volumes = self.volumes[:-1]   
        
    def updateLists(self, value):
        self.times.append(value[0])   # datetime
        self.opens.append(value[1])   # open
        self.highs.append(value[2])   # high
        self.lows.append(value[3])    # low
        self.closes.append(value[4])  # close
        self.volumes.append(value[5]) # volume
        
        
        
    # overloads
    def __str__(self):
        string = ''
        #TODO
        return 'TimeFrame(%s):\n' % self.period
    def __repr__(self):
        return 'TimeFrame(%s)' % self.period
    def __len__(self):
        return len(self.times)
    def __getitem__(self, offset):
        return (self.times[offset], self.opens[offset], self.highs[offset], self.lows[offset], self.closes[offset], self.volumes[offset])
    def __getslice__(self, low, high):
        #TODO
        return
    
if __name__=='__main__':
    
    import random
    
    s = Sma(4)
    s2 = Sma(12)
    s3 = Sma(8)
    s4 = Sma(26)
    s5 = Sma(100)
    s6 = Sma(57)
    tf = TimeFrame(1, indicators=[s, s2, s3, s4, s5, s6])
    #tf = TimeFrame(1, indicators=[s])
    
    d = datetime.datetime(2005, 1, 1, 15, 30)
    td = datetime.timedelta(0, 1)
    close = 12.20
    nrofticks = int(60 * 60 * 6.5) # one market day with one tick every second
    start = datetime.datetime.now()
    for x in xrange(nrofticks):
        c = (d, 12.34, 12.56, 12.11, close, 20192812)
        tf.handleTick(c[0], close)
        d = d + td
        if (random.random() > 0.4): close = close + random.random()/2
        else: close = close - random.random()/2
    end = datetime.datetime.now()
    diff = end - start
    dfsec = float("" + str(diff.seconds) + "." + str(diff.microseconds))
    print "Inserting %s candles took %s seconds. %s candles per second." % (nrofticks, dfsec, nrofticks / dfsec)