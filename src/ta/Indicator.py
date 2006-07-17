import datetime

# define exceptions
class IndicatorError(Exception): pass
class InvalidCandleStickError(IndicatorError): pass
class NotTupleError(InvalidCandleStickError): pass
class NotFloatError(InvalidCandleStickError): pass
class InvalidDateTimeError(InvalidCandleStickError): pass
class IndicatorSignalError(IndicatorError): pass

class Indicator:
    def __init__(self, parameter, *args, **kwargs):
        self.parameter = parameter
        self.validateParameter(self.parameter)
        self.row = 4 # close
        if args: self.row = args[0]
        for k,v in kwargs.items():
            setattr(self, k, v)
        
        self.times = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
         
    def append(self, candle):
        # check if valid input
        self.validateInput(candle)
        # check for virtual candle
        if len(self.times) > 0 and self.times[-1] == candle[0]:
            self.revertToPreviousState()
        self.calculate(candle)
        self.updateLists(candle)
        self.sanityCheck(candle)
        
    def revertToPreviousState(self):
        # remove previous virtual candle
        self.times = self.times[:-1]
        self.opens = self.opens[:-1]
        self.highs = self.highs[:-1]
        self.lows = self.lows[:-1]
        self.closes = self.closes[:-1]
        self.volumes = self.volumes[:-1]
            
    def calculate(self, candle):
        pass
    
    def validateParameter(self, parameter):
        pass
    
    def sanityCheck(self, candle):
        pass
    
    def updateLists(self, candle):
        self.times.append(candle[0])   # datetime
        self.opens.append(candle[1])   # open
        self.highs.append(candle[2])   # high
        self.lows.append(candle[3])    # low
        self.closes.append(candle[4])  # close
        self.volumes.append(candle[5]) # volume
        
    def signal(self):
        signals = getattr(self, 'signals', 'notset')
        if signals == 'notset': raise IndicatorSignalError, 'signal method called without a signals attribute'
        if type(signals) is not tuple and type(signals) is not list:
            raise IndicatorSignalError, 'signals should be a tuple or a list; input: %s' % (signals, )
        for name in signals:
            if not hasattr(self, 'signal_' + name): raise IndicatorSignalError, 'signal_%s method does not exist' % (name, )
            else: 
                method = getattr(self, 'signal_' + name)
                if callable(method):
                    if method() == False: return False
                    elif method() != True: raise IndicatorSignalError, 'signal_%s should return True or False' % (name, )
                else: raise IndicatorSignalError, 'signal_%s is not a callable method' % (name, )
        return True
    
    def validateInput(self, candle):
        if type(candle) is not tuple:
            raise NotTupleError, 'invalid input: should be a tuple (d, o, h, l, c, v); input: %s' % (candle, )
        if len(candle) < 6:
            raise InvalidCandleStickError, 'invalid input: tuple length should be 6 or more; input: %s' % (candle, )
        if not type(candle[0]) is datetime.datetime:
            raise InvalidDateTimeError, 'invalid input: tuple element [0] should be a datetime; input: %s' % (candle[0], )
        for i in range(1,5):
            if type(candle[i]) is not int and type(candle[i]) is not float:
                raise InvalidCandleStickError, 'invalid input: tuple element [%s] is not int or float; input: %s' % (i, candle[i])
            elif candle[i] <= 0:
                raise InvalidCandleStickError, 'invalid input: tuple element [%s] is equal or less than 0; input: %s' % (i, candle[i])
        if candle[2] < candle[3]:
            raise InvalidCandleStickError, 'invalid input: high: %s is lower than low: %s' % (candle[2], candle[3])
        if candle[1] > candle[2] or candle[1] < candle[3]:
            raise InvalidCandleStickError, 'invalid input: open (%s) is outside high (%s) - low (%s) range' % (candle[1], candle[2], candle[3])
        if candle[4] > candle[2] or candle[4] < candle[3]:
            raise InvalidCandleStickError, 'invalid input: close (%s) is outside high (%s) - low (%s) range' % (candle[4], candle[2], candle[3])
        if len(self.times) > 0 and self.times[-1] != None and candle[0] < self.times[-1]:
            raise InvalidDateTimeError, 'invalid input: tuple element [0] (datetime) should be equal or greater than previous: %s; input: %s' % (self.times[-1], candle[0])  
        if type(candle[5]) is not int:
            raise InvalidCandleStickError, 'invalid input: volume should be int; input: %s' % candle[5]

