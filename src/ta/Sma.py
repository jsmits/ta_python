#import Logger
import datetime
from Indicator import *

#logger = Logger.logger()

class Sma(Indicator):
    """ calculates Smooth Moving Average (SMA) indicator class """
   
    def __init__(self, parameter, *args, **kwargs):
        Indicator.__init__(self, parameter, *args, **kwargs)
        self.input = []
        self.output = []
        
    def calculate(self, candle):
        value = candle[self.row]
        self.input.append(float(value))
        outputvalue = None
        if len(self.input) >= self.parameter:
            try:    
                outputvalue = sum(self.input[(len(self.input)-self.parameter):len(self.input)]) / self.parameter
            except:
                self.input = self.input[:-1]
                raise IndicatorError, 'error calculating sma value; should never happen here'
        self.output.append(outputvalue)
        
    def revertToPreviousState(self):
        # remove previous virtual candle
        Indicator.revertToPreviousState(self)
        self.input = self.input[:-1]
        self.output = self.output[:-1]
        
    def validateParameter(self, parameter):
        if type(parameter) is not int:
            raise IndicatorError, 'invalid parameter for initializing Sma instance, should be an integer; input: %s' % (self.parameter, )
        if parameter < 1:
            raise IndicatorError, 'invalid parameter for initializing Sma instance, should be an int > 0; input: %s' % (self.parameter, )
    
    # override functions
    def __str__(self):
        string = ''
        for i in xrange(len(self.input)):
            string+='%s\t%s\t%s\t%s\n' % (i+1, self.times[i], self.input[i], str(self.output[i])[:9])
        return 'Sma(%s):\n%s' % (self.parameter, string)
    def __repr__(self):
        return 'Sma(%s)' % self.parameter
    def __len__(self):
        return len(self.output)
    def __getitem__(self, offset):
        return self.output[offset]
    def __getslice__(self, low, high):
        return self.output[low:high]
    
    # signals
    def signal_crossoverup(self):
        if len(self.times) > 1 and self.input[-1] > self.output[-1] and self.input[-2] < self.output[-2]: return True
        return False

    def signal_crossoverdown(self):
        if len(self.times) > 1 and self.input[-1] < self.output[-1] and self.input[-2] > self.output[-2]: return True
        return False
