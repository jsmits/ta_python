import datetime

class Indicator:
    def __init__(self):
        self.times = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
        
        self.input = []
        self.output = []
        
        self.row = 4 # close
        
    def handleVirtualCandle(self, value):
        # revert back to previous state, remove previous virtual candle
        self.times = self.times[:-1]
        self.opens = self.opens[:-1]
        self.highs = self.highs[:-1]
        self.lows = self.lows[:-1]
        self.closes = self.closes[:-1]
        self.volumes = self.volumes[:-1]
        self.input = self.input[:-1]
        self.output = self.output[:-1]
         
    def append(self, candle):
        # check if valid input
        validateInput(candle, self.times)
        # check for virtual candle
        if len(self.times) > 0 and self.times[-1] == candle[0]:
            self.handleVirtualCandle(candle)
        if self.calculate(candle):
            self.updateLists(candle)
            self.signals()
            
    def calculate(self, value):
        pass
    
    def updateLists(self, value):
        self.times.append(value[0])   # datetime
        self.opens.append(value[1])   # open
        self.highs.append(value[2])   # high
        self.lows.append(value[3])    # low
        self.closes.append(value[4])  # close
        self.volumes.append(value[5]) # volume
        
    def signals(self):
        pass
        
    
        
# define exceptions
class IndicatorError(Exception): pass
class NotTupleError(IndicatorError): pass
class NotFloatError(IndicatorError): pass
class InvalidCandleStickError(IndicatorError): pass
class InvalidDateTimeError(IndicatorError): pass

def validateInput(value, times):
    if type(value) is not tuple:
        raise NotTupleError, 'invalid input: should be a tuple (d, o, h, l, c, v); input: %s' % (value,)
    if len(value) != 6:
        raise InvalidCandleStickError, 'invalid input: tuple length should be 6; input: %s' % (value,)
    if not type(value[0]) is datetime.datetime:
        raise InvalidDateTimeError, 'invalid input: tuple element [0] should be a datetime; input: %s' % (value[0],)
    for i in range(1,5):
        if type(value[i]) is not int and type(value[i]) is not float:
            raise InvalidCandleStickError, 'invalid input: tuple element [%s] is not int or float; input: %s' % (i,value[i])
    if len(times) > 0 and value[0] < times[-1]:
        raise InvalidDateTimeError, 'invalid input: tuple element [0] (datetime) should be equal or greater than previous: %s; input: %s' % (times[-1], value[0])  
    if type(value[5]) is not int:
        raise InvalidCandleStickError, 'invalid input: volume should be int; input: %s' % value[5]
