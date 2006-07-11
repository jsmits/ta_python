from Indicator import *

class Ema(Indicator):
    """ Exponential Moving Average (EMA) indicator class
            formula:    ((close - prev) * K) + prev """
    
    def __init__(self, parameter, *args, **kwargs):
        Indicator.__init__(self, parameter, *args, **kwargs)
        self.input = []
        self.output = []
        
    def calculate(self, candle):
        value = candle[self.row]
        self.input.append(float(value))
        outputvalue = None
        if len(self.input) == self.parameter: # first one is a sma
            try:
                outputvalue = sum(self.input[(len(self.input)-self.parameter):len(self.input)]) / self.parameter
            except:
                self.input = self.input[:-1]
                raise IndicatorError, 'error calculating first sma in ema; reverting input data back to previous state'
        if len(self.input) > self.parameter:
            try:    
                outputvalue = ((value - self.output[-1]) * (2.0 / (1+self.parameter))) + self.output[-1]
            except:
                self.input = self.input[:-1]
                raise IndicatorError, 'error calculating ema value; reverting input data back to previous state'
        self.output.append(outputvalue)

    def revertToPreviousState(self):
        # remove previous virtual candle
        Indicator.revertToPreviousState(self)
        self.input = self.input[:-1]
        self.output = self.output[:-1]
    
    def validateParameter(self, parameter):
        if type(parameter) is not int:
            raise IndicatorError, 'invalid parameter for initializing Ema instance, should be an integer; input: %s' % (self.parameter, )
        if parameter < 1:
            raise IndicatorError, 'invalid parameter for initializing Ema instance, should be an int > 0; input: %s' % (self.parameter, )
    
    # override functions
    def __str__(self):
        string = ''
        for i in xrange(len(self.input)):
            string+='%s\t%s\t%s\t%s\n' % (i+1, self.times[i], self.input[i], self.output[i])
        return 'Ema(%s):\n%s' % (self.parameter, string)
    def __repr__(self):
        return 'Ema(%s)' % self.parameter
    def __len__(self):
        return len(self.output)
    def __getitem__(self, offset):
        return self.output[offset]
    def __getslice__(self, low, high):
        return self.output[low:high]
    
class EmaMacd(Ema):
    """ Exponential Moving Average (EMA) of MACD indicator class
            formula:    ((close - prev) * K) + prev """
    def __init__(self, parameter, *args, **kwargs):
        Ema.__init__(self, parameter, *args, **kwargs)
        self.firstfilledindex = None
   
    def append(self, candle):
        if candle == None: 
            if not self.firstfilledindex:
                self.times.append(None)
                self.opens.append(None)
                self.highs.append(None)
                self.lows.append(None)
                self.closes.append(None)
                self.volumes.append(None)
                self.input.append(None)
                self.output.append(None)
                return
            else:
                raise IndicatorError, 'invalid input; None appended after real values in list'
        # need to know if it is a valid candle
        validateEmaMacdInput(candle, self.times)
        if self.firstfilledindex != 0 and not self.firstfilledindex:
            self.firstfilledindex = len(self.output)
        # check for virtual candle
        if len(self.times) > 0 and self.times[-1] == candle[0]:
            self.revertToPreviousState()
        self.calculate(candle)
        self.updateLists(candle)
        if self.times == None:
            self.firstfilledindex = None
    
    def revertToPreviousState(self):
        # remove previous virtual candle
        Indicator.revertToPreviousState(self)
        self.input = self.input[:-1]
        self.output = self.output[:-1]
        
    def calculate(self, candle):
        value = candle[self.row]
        self.input.append(float(value))
        outputvalue = None
        if len(self.input) == self.firstfilledindex + self.parameter: # first one is a sma
            try:
                outputvalue = sum(self.input[(len(self.input)-self.parameter):len(self.input)]) / self.parameter
            except:
                self.input = self.input[:-1]
                raise IndicatorError, 'error calculating first sma in ema_macd; reverting input data back to previous state'
        if len(self.input) > self.firstfilledindex + self.parameter:
            try:    
                outputvalue = ((value - self.output[-1]) * (2.0 / (1+self.parameter))) + self.output[-1]
            except:
                self.input = self.input[:-1]
                raise IndicatorError, 'error calculating ema_macd value; reverting input data back to previous state'
        self.output.append(outputvalue)
    
    # override functions
    def __str__(self):
        string = ''
        for i in xrange(len(self.input)):
            string+='%s\t%s\t%s\t%s\n' % (i+1, self.times[i], self.input[i], self.output[i])
        return 'EmaMacd(%s):\n%s' % (self.parameter, string)
    def __repr__(self):
        return 'EmaMacd(%s)' % self.parameter
    def __len__(self):
        return len(self.output)
    def __getitem__(self, offset):
        return self.output[offset]
    def __getslice__(self, low, high):
        return self.output[low:high]
    
def validateEmaMacdInput(candle, times):
    if type(candle) is not tuple:
        raise NotTupleError, 'invalid input: should be a tuple (d, o, h, l, c, v); input: %s' % (candle, )
    if len(candle) < 6:
        raise InvalidCandleStickError, 'invalid input: tuple length should be 6 or more; input: %s' % (candle, )
    if not type(candle[0]) is datetime.datetime:
        raise InvalidDateTimeError, 'invalid input: tuple element [0] should be a datetime; input: %s' % (candle[0], )
    for i in range(1,5):
        if type(candle[i]) is not int and type(candle[i]) is not float:
            raise InvalidCandleStickError, 'invalid input: tuple element [%s] is not int or float; input: %s' % (i, candle[i])
    if candle[2] < candle[3]:
        raise InvalidCandleStickError, 'invalid input: high: %s is lower than low: %s' % (candle[2], candle[3])
    if candle[1] > candle[2] or candle[1] < candle[3]:
        raise InvalidCandleStickError, 'invalid input: open (%s) is outside high (%s) - low (%s) range' % (candle[1], candle[2], candle[3])
    if candle[4] > candle[2] or candle[4] < candle[3]:
        raise InvalidCandleStickError, 'invalid input: close (%s) is outside high (%s) - low (%s) range' % (candle[4], candle[2], candle[3])
    if len(times) > 0 and times[-1] != None and candle[0] < times[-1]:
        raise InvalidDateTimeError, 'invalid input: tuple element [0] (datetime) should be equal or greater than previous: %s; input: %s' % (times[-1], candle[0])  
    if type(candle[5]) is not int:
        raise InvalidCandleStickError, 'invalid input: volume should be int; input: %s' % candle[5]
    
if __name__=='__main__':
    ind = Ema(6)
    #input = [12.23, 12.34, 12.33, 12.35, 12.37, 12.24, 12.21, 12.11, 12.05, 11.85]
    import datetime
    input = [(datetime.datetime(2006, 5, 1), 12.34, 12.56, 12.11, 12.20, 2010912),
             (datetime.datetime(2006, 5, 2), 12.24, 12.48, 12.20, 12.22, 8791029),
             (datetime.datetime(2006, 5, 3), 12.18, 12.20, 11.88, 12.16, 5434255),
             (datetime.datetime(2006, 5, 4), 12.24, 12.68, 12.24, 12.38, 8734251),
             (datetime.datetime(2006, 5, 5), 12.30, 12.88, 12.28, 12.57, 3637262),
             (datetime.datetime(2006, 5, 8), 12.34, 12.56, 12.11, 12.20, 2010912),
             (datetime.datetime(2006, 5, 9), 12.24, 12.48, 12.20, 12.22, 8791029),
             (datetime.datetime(2006, 5, 10), 12.18, 12.20, 11.88, 12.16, 5434255),
             (datetime.datetime(2006, 5, 11), 12.24, 12.68, 12.24, 12.38, 8734251),
             (datetime.datetime(2006, 5, 12), 12.30, 12.88, 12.28, 12.57, 3637262),
             (datetime.datetime(2006, 5, 15), 12.34, 12.56, 12.11, 12.20, 2010912),
             (datetime.datetime(2006, 5, 16), 12.24, 12.48, 12.20, 12.22, 8791029),
             (datetime.datetime(2006, 5, 17), 12.18, 12.20, 11.88, 12.16, 5434255),
             (datetime.datetime(2006, 5, 18), 12.24, 12.68, 12.24, 12.38, 8734251),
             (datetime.datetime(2006, 5, 19), 12.30, 12.88, 12.28, 12.57, 3637262),
          ]
    for i in input:
        ind.append(i)
    print ind
    
    ind = EmaMacd(6)
    input = [None]*4 + input
    for i in input:
        ind.append(i)
    print ind
    
    