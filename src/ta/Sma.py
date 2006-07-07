#import Logger
import datetime
from Indicator import *

#logger = Logger.logger()

class Sma(Indicator):
    # signal constants
    NO_SIGNAL = 0
    CO = 1
    # status constants
    ABOVE = 1
    EQUAL = 0
    BELOW = -1
    
    def __init__(self, parameter, *args, **kwargs):
        Indicator.__init__(self, parameter, *args, **kwargs)
        self.input = []
        self.output = []
        self.signal = []
        self.status = []
        
    def calculate(self, value):
        value = value[self.row]
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
    
    def signals(self):
        if len(self.output) < 2:
            self.signal.append(self.NO_SIGNAL)
            self.status.append(None)
        elif self.output[-1] == None or self.output[-2] == None:
            self.signal.append(self.NO_SIGNAL)
            self.status.append(None)
        # CO ABOVE
        elif (self.input[-1] > self.output[-1]) and (self.input[-2] < self.output[-2]):
            self.signal.append(self.CO)
            self.status.append(self.ABOVE)
            raise Signal, self
        # CO BELOW
        elif (self.input[-1] < self.output[-1]) and (self.input[-2] > self.output[-2]):
            self.signal.append(self.CO)
            self.status.append(self.BELOW)
            raise Signal, self
        # NO_SIGNAL
        else:
            self.signal.append(self.NO_SIGNAL)
            if self.input[-1] > self.output[-1]: self.status.append(self.ABOVE)
            if self.input[-1] == self.output[-1]: self.status.append(self.EQUAL)
            if self.input[-1] < self.output[-1]: self.status.append(self.BELOW)
    
    def getSignal(self):
        if len(self.signal) > 0: return self.signal[-1]
        else: return None
        
    def getStatus(self):
        if len(self.status) > 0: return self.status[-1]
        else: return None
    
    # override functions
    def __str__(self):
        string = ''
        for i in xrange(len(self.input)):
            string+='%s\t%s\t%s\t%s\t%s\t%s\n' % (i+1, self.times[i], self.input[i], str(self.output[i])[:9], self.signal[i], self.status[i])
        return 'Sma(%s):\n%s' % (self.parameter, string)
    def __repr__(self):
        return 'Sma(%s)' % self.parameter
    def __len__(self):
        return len(self.output)
    def __getitem__(self, offset):
        return self.output[offset]
    def __getslice__(self, low, high):
        return self.output[low:high]
