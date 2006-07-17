from Indicator import *

class Tops(Indicator):
    """ calculates tops
        coding:     0 - no top 
                    1 - L; 11 - LL; 21 - EL; 31 - HL
                    2 - H; 12 - LH; 22 - EH; 32 - HH
       """
    # signal constants   
    L  =  1
    LL = 11
    EL = 21
    HL = 31
    H  =  2
    LH = 12
    EH = 22
    HH = 32
    
    def __init__(self, *args, **kwargs):
        Indicator.__init__(self, None, *args, **kwargs)
       
        self.inputhigh = []
        self.inputlow = []
        self.output = []
        
        self.report = True
        
        self.mark = 0, 0
        self.ph = [] # previous high list
        self.pl = [] # previous low list
        self.last_fixed = None 
        
        # for reverting back to previous state in case of a virtual candle
        self.previousoutput = []
        self.previousmark = 0, 0
        self.previousph = [] # previous high list
        self.previouspl = [] # previous low list
        self.previouslast_fixed = None 
        
    def calculate(self, candle):
        # copy current state to previous state
        self.previousoutput = list(self.output)
        self.previousmark = self.mark
        self.previousph = list(self.ph)
        self.previouspl = list(self.pl)
        self.previouslast_fixed = self.last_fixed
        
        high = float(candle[2])
        low = float(candle[3])
        self.inputhigh.append(high)
        self.inputlow.append(low)
        
        if len(self.inputhigh)==1:
            self.output.append(0)
            return
        
        if high <= self.inputhigh[self.mark[0]] and low >= self.inputlow[self.mark[0]]: # inside  bar
            self.output.append(0)
            return
        if high  > self.inputhigh[self.mark[0]] and low  < self.inputlow[self.mark[0]]: # outside bar
            if self.ph == [] and self.pl == []:
                self.output.append(0)
                self.mark = len(self.output)-1, 0
            else:
                self.output.append(0) # added new code line 17-7-2006 !!!
                self.output[self.mark[0]] = 0
                for j in reversed(range(len(self.output)-1)):
                    if self.inputhigh[j] > high or self.inputlow[j] < low: # first non-inclusive bar
                        break
                count = 0
                for k in range(j+1, len(self.output)-1): # checking for inbetween tops
                    if self.output[k] != 0: # top found
                        count += 1
                        if self.output[k] in [self.L, self.LL, self.EL, self.HL]: self.pl.remove(k) # removing top indexes from list
                        if self.output[k] in [self.H, self.LH, self.EH, self.HH]: self.ph.remove(k) # idem
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
            return
        if high  > self.inputhigh[self.mark[0]] and low >= self.inputlow[self.mark[0]]: # upbar
            if self.mark[1]  < 2: # upbar with previous indifferent or low mark
                if self.pl == []: self.output[self.mark[0]] = self.L # L
                else:
                    if    self.inputlow[self.mark[0]]  <   self.inputlow[self.pl[-1]]: self.output[self.mark[0]] = self.LL # LL
                    elif  self.inputlow[self.mark[0]] ==   self.inputlow[self.pl[-1]]: self.output[self.mark[0]] = self.EL # EL
                    elif  self.inputlow[self.mark[0]]  >   self.inputlow[self.pl[-1]]: self.output[self.mark[0]] = self.HL # HL
                self.pl.append(self.mark[0])
                self.last_fixed = self.mark[0], 1
                self.mark = len(self.output), 2
                self.output.append(0)
            elif self.mark[1] == 2: # upbar with previous high mark
                self.output[self.mark[0]] = 0 # reset previous mark
                self.mark = len(self.output), 2
                self.output.append(0)
            return
        if high <= self.inputhigh[self.mark[0]] and low  < self.inputlow[self.mark[0]]: # downbar
            if self.mark[1] != 1: # downbar with previous indifferent or high mark
                if self.ph == []: self.output[self.mark[0]] = self.H # H
                else:
                    if   self.inputhigh[self.mark[0]]  < self.inputhigh[self.ph[-1]]: self.output[self.mark[0]] = self.LH # LH
                    elif self.inputhigh[self.mark[0]] == self.inputhigh[self.ph[-1]]: self.output[self.mark[0]] = self.EH # EH
                    elif self.inputhigh[self.mark[0]]  > self.inputhigh[self.ph[-1]]: self.output[self.mark[0]] = self.HH # HH
                self.ph.append(self.mark[0])
                self.last_fixed = self.mark[0], 2
                self.mark = len(self.output), 1
                self.output.append(0)
            elif self.mark[1] == 1: # downbar with previous low mark
                self.output[self.mark[0]] = 0 # reset previous mark
                self.mark = len(self.output), 1
                self.output.append(0)
            return
    
    # to be made
    def revertToPreviousState(self):
        # remove previous virtual candle
        Indicator.revertToPreviousState(self)
        self.inputlow = self.inputlow[:-1]
        self.inputhigh = self.inputhigh[:-1]
        self.output = list(self.previousoutput)
        self.mark = self.previousmark
        self.ph = list(self.previousph)
        self.pl = list(self.previouspl)
        self.last_fixed = self.previouslast_fixed
    
    def sanityCheck(self, candle):
        if (len(self.output) != len(self.times)) and self.report == True:
            print "Output length out of sync with input; candle %s, self.times length: %s" % (candle, len(self.times))
            self.report = False
        
    # overloads
    def __str__(self):
        string = ''
        for i in xrange(len(self.inputhigh)):
            string+='%s\t%s\t%s\t%s\n' % (i+1, self.inputhigh[i], self.inputlow[i], self.output[i])
        return 'Tops():\n%s' % (string)
    def __repr__(self):
        return 'Tops()'
    def __len__(self):
        return len(self.output)
    def __getitem__(self, offset):
        return self.output[offset]
    def __getslice__(self, low, high):
        return self.output[low:high]
    
    # signals
    def tops(self, number=6):
        result = []
        for i in xrange(len(self.output)-1,-1,-1):
            if self.output[i] != 0: 
                result.insert(0, self.output[i]) # 'append' at the start
                if len(result) == number: break
        return tuple(result)
    
    # L HH HL variations
    def signal_ALHHHL(self):
        patterns = [(11,32,31), (21,32,31), (31,32,31)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
        
    def signal_LLHHHL(self):
        '(LL, HH, HL)'
        patterns = [(11,32,31)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
    
    def signal_LorELHHHL(self):
        '(LL or EL, HH, HL)'
        patterns = [(11,32,31), (21,32,31)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
        
    def signal_HLHHHL(self):
        '(HL, HH, HL)'
        patterns = [(31,32,31)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
        
    def signal_EorHLHHHL(self):
        '(EL or HL, HH, HL)'
        patterns = [(21,32,31), (31,32,31)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
        
    # L LH HL variations; TO-DO
    def signal_ALLHHL(self):
        patterns = [(11,12,31), (21,12,31), (31,12,31)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
        
    def signal_LLLHHL(self):
        '(LL, LH, HL)'
        patterns = [(11,12,31)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
    
    def signal_LorELLHHL(self):
        '(LL or EL, LH, HL)'
        patterns = [(11,12,31), (21,12,31)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
        
    def signal_HLLHHL(self):
        '(HL, LH, HL)'
        patterns = [(31,12,31)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
        
    def signal_EorHLLHHL(self):
        '(EL or HL, LH, HL)'
        patterns = [(21,12,31), (31,12,31)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
    
    # H LL LH variations
    def signal_AHLLLH(self):
        '(LH or EH or HH, LL, LH)'
        patterns = [(12,11,12), (22,11,12), (32,11,12)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
        
    def signal_HLLLLH(self):
        '(HL, LL, LH)'
        patterns = [(32,11,12)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
    
    def signal_LorEHLLLH(self):
        '(LH or EH, LL, LH)'
        patterns = [(12,11,12), (22,11,12)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
        
    def signal_LHLLLH(self):
        '(LH, LL, LH)'
        patterns = [(12,11,12)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
        
    def signal_EorHHLLLH(self):
        '(EH or HH, LL, LH)'
        patterns = [(22,11,12), (32,11,12)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
        
    # H HL LH variations
    def signal_AHHLLH(self):
        '(LH or EH or HH, HL, LH)'
        patterns = [(12,31,12), (22,31,12), (32,31,12)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
        
    def signal_HLHLLH(self):
        '(HL, HL, LH)'
        patterns = [(32,31,12)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
    
    def signal_LorEHHLLH(self):
        '(LH or EH, HL, LH)'
        patterns = [(12,31,12), (22,31,12)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
        
    def signal_LHHLLH(self):
        '(LH, HL, LH)'
        patterns = [(12,31,12)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False
        
    def signal_EorHHHLLH(self):
        '(EH or HH, HL, LH)'
        patterns = [(22,31,12), (32,31,12)]
        toppattern = self.tops(3)
        if toppattern in patterns: return True
        else: return False

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
             (datetime.datetime(2006, 5, 10), 12.21, 12.40, 12.21, 12.21, 5434255),
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