import logging
import logging.config

class Tops:
    """ calculates tops
        coding:     0 - no top 
                    1 - L; 11 - LL; 21 - EL; 31 - HL
                    2 - H; 12 - LH; 22 - EH; 32 - HH
       """
    def __init__(self, *args):
        self.highs = []
        self.lows = []
        self.closes = []
        self.output = []
        
        self.mark = 0, 0
        self.ph = [] # previous high list
        self.pl = [] # previous low list
        self.last_fixed = None 
        
        logging.config.fileConfig("../logging.conf")
        self.logger = logging.getLogger("Indicator")
        
    def append(self, value):
        # check if valid input
        if not self._validate(value): return
        if self._calculate(value): return self.output[-1]
        
    def _validate(self, value):
        if not type(value) is tuple:
            self.logger.debug('invalid input: %s; should be a candle data tuple' % value) 
            return False
        else: 
            return True # TODO check high and low
        
    def _calculate(self, value):
        high = float(value[2])
        low = float(value[3])
        self.highs.append(high)
        self.lows.append(low)
        
        if len(self.highs)==0:
            self.output.append(0)
            return True
        
        if high <= self.highs[self.mark[0]] and low >= self.lows[self.mark[0]]: # inside  bar
            self.output.append(0)
            return True
        if high  > self.highs[self.mark[0]] and low  < self.lows[self.mark[0]]: # outside bar
            if self.ph == [] and self.pl == []:
                self.output.append(0)
                self.mark = len(self.output)-1, 0
            else:
                self.output[self.mark[0]] = 0
                for j in reversed(range(len(self.output)-1)):
                    if self.highs[j] > high or self.lows[j] < low: # first non-inclusive bar
                        break
                count = 0
                for k in range(j+1, len(self.output)-1): # checking for inbetween tops
                    if self.output[k] != 0: # top found
                        count += 1
                        if self.output[k] in [1, 11, 21, 31]: self.pl.remove(k) # removing top indexes from list
                        if self.output[k] in [2, 12, 22, 32]: self.ph.remove(k) # idem
                        self.output[k] = 0 # reset top
                if count > 0:
                    if len(self.pl) and len(self.ph):
                        if (self.pl[-1] > self.ph[-1]): # if true, low is most recent
                            self.last_fixed = self.pl[-1], 1
                            self.mark = len(self.output)-1, 2
                        elif (self.ph[-1] > self.pl[-1]): # high is most recent
                            self.last_fixed = self.ph[-1], 2
                            self.mark = len(self.output)-1, 1
                        elif len(self.pl) and not len(self.ph):
                            self.last_fixed = self.pl[-1], 1
                            self.mark = len(self.output)-1, 2
                        elif len(self.ph) and not len(self.pl):
                            self.last_fixed = self.ph[-1], 2
                            self.mark = len(self.output)-1, 1
                        elif not len(self.pl) and not len(self.ph):
                            self.last_fixed = None
                            self.mark = len(self.output)-1, 0 # current outside bar has become indifferent
                if count == 0:
                    self.mark = len(self.output)-1, self.mark[1] # set same signal to current outside bar
            return True
        if high  > self.highs[self.mark[0]] and low >= self.lows[self.mark[0]]: # upbar
            if self.mark[1]  < 2: # upbar with previous indifferent or low mark
                if self.pl == []: self.output[self.mark[0]] = 1 # L
                else:
                    if    self.lows[self.mark[0]]  <   self.lows[self.pl[-1]]: self.output[self.mark[0]] = 11 # LL
                    elif  self.lows[self.mark[0]] ==   self.lows[self.pl[-1]]: self.output[self.mark[0]] = 21 # EL
                    elif  self.lows[self.mark[0]]  >   self.lows[self.pl[-1]]: self.output[self.mark[0]] = 31 # HL
                self.pl.append(self.mark[0])
                self.last_fixed = self.mark[0], 1
                self.mark = len(self.output), 2
                self.output.append(0)
            elif self.mark[1] == 2: # upbar with previous high mark
                self.output[self.mark[0]] = 0 # reset previous mark
                self.mark = len(self.output), 2
                self.output.append(0)
            return True
        if high <= self.highs[self.mark[0]] and low  < self.lows[self.mark[0]]: # downbar
            if self.mark[1] != 1: # downbar with previous indifferent or high mark
                if self.ph == []: self.output[self.mark[0]] = 2 # H
                else:
                    if   self.highs[self.mark[0]]  < self.highs[self.ph[-1]]: self.output[self.mark[0]] = 12 # LH
                    elif self.highs[self.mark[0]] == self.highs[self.ph[-1]]: self.output[self.mark[0]] = 22 # EH
                    elif self.highs[self.mark[0]]  > self.highs[self.ph[-1]]: self.output[self.mark[0]] = 32 # HH
                self.ph.append(self.mark[0])
                self.last_fixed = self.mark[0], 2
                self.mark = len(self.output), 1
                self.output.append(0)
            elif self.mark[1] == 1: # downbar with previous low mark
                self.output[self.mark[0]] = 0 # reset previous mark
                self.mark = len(self.output), 1
                self.output.append(0)
            return True
        
    # overloads
    def __str__(self):
        string = ''
        for i in xrange(len(self.highs)):
            string+='%s\t%s\t%s\t%s\n' % (i+1, self.highs[i], self.lows[i], self.output[i])
        return 'Tops():\n%s' % (string)
    def __repr__(self):
        return 'Tops()'
    def __len__(self):
        return len(self.output)
    def __getitem__(self, offset):
        return self.output[offset]
    def __getslice__(self, low, high):
        return self.output[low:high]

if __name__=='__main__':
    ind = Tops()
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