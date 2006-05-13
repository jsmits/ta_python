import logging
import logging.config

class Atr:
    def __init__(self, parameter, *args):
        self.parameter = parameter
        self.highs = []
        self.lows = []
        self.closes = []
        self.tr = []
        self.output = []
        
        logging.config.fileConfig("logging.conf")
        self.logger = logging.getLogger("Indicator")
        
    def append(self, value):
        # check if valid input
        if not self._validate(value): return
        if self._calculate(value): return self.output[-1]
        
    def _validate(self, value):
        if not type(value) is tuple:
            self.logger.debug('invalid input: %s; should be tuple' % value) 
            return False
        else:
            try:
                if not type(value[2]) is float and not type(value[2]) is int:
                    self.logger.debug('invalid input: %s; high should be float or int' % value[2])
                    return False
                if not type(value[3]) is float and not type(value[3]) is int:
                    self.logger.debug('invalid input: %s; low should be float or int' % value[3])
                    return False
                if not type(value[4]) is float and not type(value[4]) is int:
                    self.logger.debug('invalid input: %s; close should be float or int' % value[4])
                    return False
            except:
                self.logger.debug('error validating high, low, close data from %s' % value)
                return False
        return True
        
    def _calculate(self, value):
        high = float(value[2])
        low = float(value[3])
        close = float(value[4])
        
        self.highs.append(high)
        self.lows.append(low)
        self.closes.append(close)
        
        if len(self.highs) == 1:
            tr = high - low # (high - low) = initial tr
        else:
            pclose = self.closes[-2]
            tr = max(high - low, abs(high - pclose), abs(low - pclose))
        self.tr.append(tr)
        
        outputvalue = tr
        if len(self.tr) >= self.parameter:
            try:    
                patr = self.output[-1]
                atr = ((patr * (self.parameter - 1)) + self.tr[-1]) / self.parameter
                outputvalue = atr
            except:
                self.logger.debug('error calculating atr value; reverting input data back to previous state')
                self.highs = self.highs[:-1]
                self.lows = self.lows[:-1]
                self.closes = self.closes[:-1]
                self.tr = self.tr[:-1]
                return False
        self.output.append(outputvalue)
        return True
    
    # overloads
    def __str__(self):
        string = ''
        for i in xrange(len(self.highs)):
            string+='%s\t%s\t%s\t%s\t%s\t%s\n' % (i+1, self.highs[i], self.lows[i], self.closes[i], self.tr[i], self.output[i])
        return 'Atr(%s):\n%s' % (self.parameter, string)
    def __repr__(self):
        return 'Atr(%s)' % self.parameter
    def __len__(self):
        return len(self.output)
    def __getitem__(self, offset):
        return self.output[offset]
    def __getslice__(self, low, high):
        return self.output[low:high]

if __name__=='__main__':
    ind = Atr(4)
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