from Indicator import *

class Atr(Indicator):
    """ calculates Average True Range indicator
            input:      parameter = integer """
    def __init__(self, parameter, *args, **kwargs):
        Indicator.__init__(self, parameter, *args, **kwargs)
   
        self.tr = []
        self.output = []
        
    def calculate(self, candle):
        
        high = float(candle[2])
        low = float(candle[3])
        
        if len(self.highs) == 0:
            tr = high - low # (high - low) = initial tr
        else:
            pclose = self.closes[-1]
            tr = max(high - low, abs(high - pclose), abs(low - pclose))
        self.tr.append(tr)
        
        outputvalue = tr
        if len(self.tr) >= self.parameter:
            try:    
                patr = self.output[-1]
                atr = ((patr * (self.parameter - 1)) + self.tr[-1]) / self.parameter
                outputvalue = atr
            except:
                self.tr = self.tr[:-1]
                raise IndicatorError, 'error calculating atr value; reverting tr data back to previous state'
        self.output.append(outputvalue)
        
    def revertToPreviousState(self):
        # remove previous virtual candle
        Indicator.revertToPreviousState(self)
        self.tr = self.tr[:-1]
        self.output = self.output[:-1]
        
    def validateParameter(self, parameter):
        if type(parameter) is not int:
            raise IndicatorError, 'invalid parameter for initializing Atr instance, should be an integer; input: %s' % (self.parameter, )
        if parameter < 1:
            raise IndicatorError, 'invalid parameter for initializing Atr instance, should be an int > 0; input: %s' % (self.parameter, )
    
    def getAtr(self):
        if len(self.output) > 0: return self.output[-1]
        else: return None
    
    # overrided functions
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