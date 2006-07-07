from Indicator import *

class Ema(Indicator):
    """ Exponential Moving Average (EMA) indicator class
            formula:    ((close - prev) * K) + prev """
    def __init__(self, parameter, *args, **kwargs):
        Indicator.__init__(self, parameter, *args, **kwargs)
        self.input = []
        self.output = []
        self.signal = []
        self.status = []
        self.firstfilledindex = None
   
    ## to be looked at; does not work yet
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
        # put validateInput code here and get it out of Indicator append, same in Sma
        if self.firstfilledindex != 0 and not self.firstfilledindex:
            self.firstfilledindex = len(self.output)
        Indicator.append(self, candle)
        
    def calculate(self, candle):
        value = candle[self.row]
        self.input.append(float(value))
        outputvalue = None
        if len(self.input) == self.firstfilledindex + self.parameter: # first one is a sma
            try:
                outputvalue = sum(self.input[(len(self.input)-self.parameter):len(self.input)]) / self.parameter
            except:
                self.input = self.input[:-1]
                raise IndicatorError, 'error calculating first sma in ema; reverting input data back to previous state'
        if len(self.input) > self.firstfilledindex + self.parameter:
            try:    
                outputvalue = ((value - self.output[-1]) * (2.0 / (1+self.parameter))) + self.output[-1]
            except:
                self.input = self.input[:-1]
                raise IndicatorError, 'error calculating ema value; reverting input data back to previous state'
        self.output.append(outputvalue)
    
    # override functions
    def __str__(self):
        string = ''
        for i in xrange(len(self.input)):
            string+='%s\t%s\t%s\n' % (i+1, self.input[i], self.output[i])
        return 'Ema(%s):\n%s' % (self.parameter, string)
    def __repr__(self):
        return 'Ema(%s)' % self.parameter
    def __len__(self):
        return len(self.output)
    def __getitem__(self, offset):
        return self.output[offset]
    def __getslice__(self, low, high):
        return self.output[low:high]