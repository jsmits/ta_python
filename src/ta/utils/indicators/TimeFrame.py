import logging
import logging.config
import os
import datetime
from Tick2Candle import Tick2Candle
from Sma import Sma

class TimeFrame:
    
    def __init__(self, ticker, period, *args, **kwargs):
        self.ticker = ticker
        self.period = period
        self.indicators = []
        
        self.candleGenerator = Tick2Candle(period)
        
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
        
    def handleTick(self, tick):
        if not self._validateTick(tick):
            # raise Error
            return
        time = tick[0]
        ticker = tick[1]
        last = tick[2]
        candles = self.candleGenerator.processTick(time, last)
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
        
    def _validateTick(self, tick):
        if type(tick) is tuple:
            if len(tick) != 3:
                self.logger.error('invalid input: tuple length should be 3 (datetime, ticker, last); input: %s' % (tick,)) 
                return False
            elif not type(tick[0]) is datetime.datetime:
                self.logger.error('invalid input: tuple element [0] should be a datetime; input: %s' % (tick[0],)) 
                return False
            elif not type(tick[1]) is int:
                self.logger.error('invalid input: tuple element [1] should be an int (ticker); input: %s' % (tick[1],)) 
                return False
            elif not (type(tick[2]) is int or type(tick[2]) is float):
                self.logger.error('invalid input: tuple element [2] should be an int or float (last); input: %s' % (tick[2],)) 
                return False
            if tick[1] != self.ticker:
                self.logger.error('invalid input: tick ticker %s does not match self.ticker %s' % (tick[1], self.ticker)) 
                return False
            return True
        else:
            self.logger.error('invalid input: should be a tuple (datetime, ticker, last); input: %s' % (tick,)) 
            return False
        
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
        return 'TimeFrame(%s, %s):\n' % (self.ticker, self.period)
    def __repr__(self):
        return 'TimeFrame(%s, %s)' % (self.ticker, self.period)
    def __len__(self):
        return len(self.times)
    def __getitem__(self, offset):
        return (self.times[offset], self.opens[offset], self.highs[offset], self.lows[offset], self.closes[offset], self.volumes[offset])
    def __getslice__(self, low, high):
        #TODO
        return
    
if __name__=='__main__':
    s = Sma(4)
    tf = TimeFrame(5555, 1, indicators=[s])
    
    ticks = [(datetime.datetime(2006,12,5,9,30,0), 12.55),
             (datetime.datetime(2006,12,5,9,30,15), 13.02),
             (datetime.datetime(2006,12,5,9,30,30), 12.53),
             (datetime.datetime(2006,12,5,9,30,45), 13.04),
             (datetime.datetime(2006,12,5,9,31,5), 13.08),
             (datetime.datetime(2006,12,5,9,34,15), 13.28),
             (datetime.datetime(2006,12,5,9,34,30), 13.05),
             (datetime.datetime(2006,12,5,9,34,35), 13.02),
             (datetime.datetime(2006,12,5,9,34,43), 12.53),
             (datetime.datetime(2006,12,5,9,35,45), 13.04),
             (datetime.datetime(2006,12,5,9,36,5), 13.08),
             (datetime.datetime(2006,12,5,9,38,15), 13.28)]
    
    start = datetime.datetime.now()
    for t in ticks:
        tf.handleTick((t[0], 5555, t[1]))
    end = datetime.datetime.now()
    diff = end - start
    dfsec = float("" + str(diff.seconds) + "." + str(diff.microseconds))
    print "Processing %s ticks took %s seconds." % (len(ticks), dfsec)