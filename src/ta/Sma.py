import Logger
import datetime
from Indicator import *

logger = Logger.logger()

class Sma(Indicator):
    
    # signal constants
    NO_SIGNAL = 0
    CO = 1
    
    # status constants
    ABOVE = 1
    EQUAL = 0
    BELOW = -1
    
    def __init__(self, parameter, *args, **kwargs):
        
        Indicator.__init__(self)
        self.parameter = parameter
        
        if args: self.row = args[0]
        
        # signal and status
        self.signal = []
        self.status = []
        
    def getSignal(self):
        if len(self.signal) > 0: return self.signal[-1]
        else: return None
        
    def getStatus(self):
        if len(self.status) > 0: return self.status[-1]
        else: return None
        
    def _calculate(self, value):
        value = value[self.row]
        self.input.append(float(value))
        outputvalue = None
        if len(self.input) >= self.parameter:
            try:    
                outputvalue = sum(self.input[(len(self.input)-self.parameter):len(self.input)]) / self.parameter
            except:
                logger.error('error calculating sma value')
                self.input = self.input[:-1] # do something with this error, should never happen here
                return False
        self.output.append(outputvalue)
        return True
    
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
        # CO BELOW
        elif (self.input[-1] < self.output[-1]) and (self.input[-2] > self.output[-2]):
            self.signal.append(self.CO)
            self.status.append(self.BELOW)
        # NO_SIGNAL
        else:
            self.signal.append(self.NO_SIGNAL)
            if self.input[-1] > self.output[-1]: self.status.append(self.ABOVE)
            if self.input[-1] == self.output[-1]: self.status.append(self.EQUAL)
            if self.input[-1] < self.output[-1]: self.status.append(self.BELOW)
    
    # overloads
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

if __name__=='__main__':
    ind = Sma(3)
    #input = [12.23, 12.34, 12.33, 12.35, 12.37, 12.24, 12.21, 12.11, 12.05, 11.85]
    import datetime
    import random
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
    d = datetime.datetime(2005, 1, 1, 9, 30)
    td = datetime.timedelta(0, 1)
    close = 12.20
    nrofticks = int(60 * 60 * 6.5) # one market day with one tick every second
    start = datetime.datetime.now()
    for x in xrange(nrofticks):
        c = (d, 12.34, 12.56, 12.11, close, 20192812)
        ind.append(c)
        d = d + td
        if (random.random() > 0.4): close = close + random.random()/2
        else: close = close - random.random()/2
    end = datetime.datetime.now()
    diff = end - start
    logger.debug(ind)
    dfsec = float("" + str(diff.seconds) + "." + str(diff.microseconds))
    logger.info("Inserting %s candles took %s seconds. %s candles per second." % (nrofticks, dfsec, nrofticks / dfsec))