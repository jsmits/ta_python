from pp import indent

class Indicators:
    
    def __init__(self):
        self.empty  = -1000

    def reset(self, ar, r):
        if r <= 5 or r >= ar.shape[0]: return # overwrite t,o,h,l,c,v and out of array protection
        if r == 'all': ar[6:ar.shape[0]] = self.empty 
        elif r > 5 and r < ar.shape[0]: ar[r] = self.empty
        
    def find_free_row(self, ar):
        for r in range(6, ar.shape[0]):
            for i in range(ar.shape[1]):
                if ar[r][i] != self.empty: break
                if i == ar.shape[1]-1: return r
        print "array is full; to add, remove some indicators"
    
    def first_cell(self, data):
        """ returns:    first non-empty index of sequence (empty defined by init variable) """
        for i in range(len(data)):
            if data[i] != self.empty:
                return i
                
    def pp(self, data):
        """ pretty print ticker (and indicator) data
            input: data = list of lists """
        print indent(data, justify='right')

    def sma(self, data, parameter, r=4):
        """ calculates Smooth Moving Average (SMA) indicator
            input:      data        = list or tuple of float or integer values
                        parameter   = single integer
            returns:    list of sma indicator with same length as data """
        ar = False
        if type(data).__name__ == 'NumArray':
            ar = True
            fr = self.find_free_row(data)
            if not fr: return # make raise error in find_free_row()
            a = data
            data = data[r] 
        if type(data) is tuple:
            if type(data[0]) is tuple and len(data[0]) == 6: # datetime,o,h,l,c,v tuple
                temp = []
                for i in range(len(data)):
                    temp.append(data[i][r])
                data = temp
            elif type(data[0]) is float or type(data[0]) is int: # tuple of single values, either float or int
                pass        
        m = parameter
        first = self.first_cell(data)
        ind = [self.empty] * (first+m-1)
        for i in range(first+m-1, len(data)):
            sma = sum(data[((i-m)+1):(i+1)]) / m
            ind.append(sma)
        if ar:
            a[fr] = ind
            return fr
        else: return ind
            
    def ema(self, data, parameter, r=4):
        """ calculates Exponential Moving Average (EMA) indicator
            formula:    ((close - prev) * K) + prev
            input:      data        = list or tuple of float or integer values
                        parameter   = single integer
            returns:    list of ema indicator with same length as data """
        ar = False
        if type(data).__name__ == 'NumArray':
            ar = True
            fr = self.find_free_row(data)
            if not fr: return # make raise error in find_free_row()
            a = data
            data = data[r] 
        if type(data) is tuple:
            if type(data[0]) is tuple and len(data[0]) == 6: # datetime,o,h,l,c,v tuple
                temp = []
                for i in range(len(data)):
                    temp.append(data[i][r])
                data = temp
            elif type(data[0]) is float or type(data[0]) is int: # tuple of single values, either float or int
                pass        
        m = parameter
        first = self.first_cell(data)
        ind = [self.empty] * (first+m-1)
        ind.append(sum(data[first:first+m]) / m) # starting with sma
        for i in range(first+m, len(data)):
            ema = ((data[i] - ind[-1]) * (2.0 / (1+m))) + ind[-1]
            ind.append(ema)
        if ar:
            a[fr] = ind
            return fr
        else: return ind

    def macd(self, data, parameter, r=4):
        """ calculates Moving Average Convergence-Divergence (MACD) indicator
            input:      data        = list or tuple of float or integer values
                        parameter   = tuple (x, y, z); where x is short term ema, y is long term ema, and z is ema of the macd
            returns:    short ema, long ema, macd, ema of macd """
        ar = False
        m = parameter
        s_ema = self.ema(data, m[0], r=r)
        l_ema  = self.ema(data, m[1], r=r)
        if type(data).__name__ == 'NumArray':
            ar = True
            fr = self.find_free_row(data)
            if not fr: return # make raise error in find_free_row()
        macd = [self.empty] * (m[1]-1) 
        if not ar:
            for i in range(m[1]-1, len(data)):
                macd.append(s_ema[i] - l_ema[i])
            macd_ema = self.ema(macd, m[2])
        if ar:
            for i in range(m[1]-1, data.shape[1]):
                data[fr][i] = data[s_ema][i] - data[l_ema][i]
            macd_ema = self.ema(data, m[2], r=fr)
            macd = fr # set macd to free row index
        return s_ema, l_ema, macd, macd_ema

    def atr(self, data, parameter):
        """ calculates Average True Range indicator
            input:      highs, lows, closes
                        parameter = integer
            returns:    atr """
        ar = False
        if type(data).__name__ == 'NumArray':
            ar = True
            fr = self.find_free_row(data)
            if not fr: return # make raise error in find_free_row()
            highs = data[2]
            lows = data[3]
            closes = data[4]
        if type(data) is tuple:
            if type(data[0]) is tuple and len(data[0]) == 6: # datetime,o,h,l,c,v tuple
                times, opens, highs, lows, closes, volumes = zip(*data)
            elif len(data) == 3 and type(data[0]) is tuple or type(data[0]) is list: # tuple or list of 3 tuples (h, l, c) ## nog beter maken
                highs = data[0]
                lows = data[1]
                closes = data[2]
        m = parameter
        tr = []
        tr.append(highs[0] - lows[0]) # (high - low) = initial tr
        ind = [self.empty] * len(highs)
        for i in range(1, len(highs)):
            high = highs[i]
            low = lows[i]
            pclose = closes[i-1]
            tr.append(max(high - low, abs(high - pclose), abs(low - pclose)))
        ind[0:m-1] = tr[0:m-1]
        for i in range(m-1, len(highs)):
            patr = ind[i-1]
            atr = ((patr * (m - 1)) + tr[i]) / m
            ind[i] = atr
        if ar:
            data[fr] = ind
            return fr
        else: return ind
   
    def tops(self, data):
        """ determines tops
            coding:     0 - no top 
                        1 - L; 11 - LL; 21 - EL; 31 - HL
                        2 - H; 12 - LH; 22 - EH; 32 - HH
            returns:    coded tops """
        ar = False
        if type(data).__name__ == 'NumArray':
            ar = True
            fr = self.find_free_row(data)
            if not fr: return # make raise error in find_free_row()
            highs = data[2]
            lows = data[3]
        if type(data) is tuple:
            if type(data[0]) is tuple and len(data[0]) == 6: # datetime,o,h,l,c,v tuple
                times, opens, highs, lows, closes, volumes = zip(*data)
            else: # tuple or list of 2 tuples (highs, lows) ## nog beter maken
                highs = data[0]
                lows = data[1]
        mark = 0, 0
        ph = [] # previous high list
        pl = [] # previous low list
        last_fixed = None 
        ind = [self.empty] * len(highs)
        ind[0] = 0
        for i in range(1, len(highs)):
            if highs[i] <= highs[mark[0]] and lows[i] >= lows[mark[0]]: # inside  bar
                ind[i] = 0
                continue
            if highs[i]  > highs[mark[0]] and lows[i]  < lows[mark[0]]: # outside bar
                if ph == [] and pl == []:
                    ind[i] = 0
                    mark = i, 0
                else:
                    ind[mark[0]] = 0
                    for j in reversed(range(i)):
                        if highs[j] > highs[i] or lows[j] < lows[i]: # first non-inclusive bar
                            break
                    count = 0
                    for k in range(j+1, i): # checking for inbetween tops
                        if ind[k] != 0: # top found
                            count += 1
                            if ind[k] in [1, 11, 21, 31]: pl.remove(k) # removing top indexes from list
                            if ind[k] in [2, 12, 22, 32]: ph.remove(k) # idem
                            ind[k] = 0 # reset top
                    if count > 0:
                        if len(pl) and len(ph):
                            if (pl[-1] > ph[-1]): # if true, low is most recent
                                last_fixed = pl[-1], 1
                                mark = i, 2
                            elif (ph[-1] > pl[-1]): # high is most recent
                                last_fixed = ph[-1], 2
                                mark = i, 1
                        elif len(pl) and not len(ph):
                            last_fixed = pl[-1], 1
                            mark = i, 2
                        elif len(ph) and not len(pl):
                            last_fixed = ph[-1], 2
                            mark = i, 1
                        elif not len(pl) and not len(ph):
                            last_fixed = None
                            mark = i, 0 # current outside bar has become indifferent
                    if count == 0:
                        mark = i, mark[1] # set same signal to current outside bar
                    continue
            if highs[i]  > highs[mark[0]] and lows[i] >= lows[mark[0]]: # upbar
                if   mark[1]  < 2: # upbar with previous indifferent or low mark
                    if pl == []: ind[mark[0]] = 1 # L
                    else:
                        if    lows[mark[0]]  <   lows[pl[-1]]: ind[mark[0]] = 11 # LL
                        elif  lows[mark[0]] ==   lows[pl[-1]]: ind[mark[0]] = 21 # EL
                        elif  lows[mark[0]]  >   lows[pl[-1]]: ind[mark[0]] = 31 # HL
                    pl.append(mark[0])
                    last_fixed = mark[0], 1
                    mark = i, 2
                    ind[i] = 0
                elif mark[1] == 2: # upbar with previous high mark
                    ind[mark[0]] = 0 # reset previous mark
                    mark = i, 2
                    ind[i] = 0
                continue
            if highs[i] <= highs[mark[0]] and lows[i]  < lows[mark[0]]: # downbar
                if mark[1] != 1: # downbar with previous indifferent or high mark
                    if ph == []: ind[mark[0]] = 2 # H
                    else:
                        if   highs[mark[0]]  < highs[ph[-1]]: ind[mark[0]] = 12 # LH
                        elif highs[mark[0]] == highs[ph[-1]]: ind[mark[0]] = 22 # EH
                        elif highs[mark[0]]  > highs[ph[-1]]: ind[mark[0]] = 32 # HH
                    ph.append(mark[0])
                    last_fixed = mark[0], 2
                    mark = i, 1
                    ind[i] = 0
                elif mark[1] == 1: # downbar with previous low mark
                    ind[mark[0]] = 0 # reset previous mark
                    mark = i, 1
                    ind[i] = 0
                continue
        if ar:
            data[fr] = ind
            return fr
        else: return ind

class Tops:
    """ test, experimental and debugging tops module """
    
    def __init__(self):
        self.empty = -1000
        pass

    def tops(self, data):
        """ determines tops
            coding:     0 - no top 
                        1 - L; 11 - LL; 21 - EL; 31 - HL
                        2 - H; 12 - LH; 22 - EH; 32 - HH
            returns:    coded tops """
        ar = False
        if type(data).__name__ == 'NumArray':
            ar = True
            fr = self.find_free_row(data)
            if not fr: return # make raise error in find_free_row()
            highs = data[2]
            lows = data[3]
        if type(data) is tuple:
            if type(data[0]) is tuple and len(data[0]) == 6: # datetime,o,h,l,c,v tuple
                times, opens, highs, lows, closes, volumes = zip(*data)
            elif len(data) == 2 and type(data[0]) is tuple or type(data[0]) is list: # tuple or list of 2 tuples (highs, lows) ## nog beter maken
                highs = data[0]
                lows = data[1]
        mark = 0, 0
        ph = []
        pl = []
        last_fixed = None 
        ind = [self.empty] * len(highs)
        ind[0] = 0
        for i in range(1, len(highs)):
            print "%i)\t%.2f\t%.2f" % (i, highs[i], lows[i])
            if highs[i] <= highs[mark[0]] and lows[i] >= lows[mark[0]]: # inside  bar
                print "\tinside bar"
                ind[i] = 0
                continue
            if highs[i]  > highs[mark[0]] and lows[i]  < lows[mark[0]]: # outside bar
                if ph == [] and pl == []:
                    print "\toutside bar without previous high or low"
                    ind[i] = 0
                    mark = i, 0
                else:
                    print "\toutside bar"
                    ind[mark[0]] = 0
                    for j in reversed(range(i)):
                        if highs[j] > highs[i] or lows[j] < lows[i]: # first non-inclusive bar
                            print "\tfirst non-inclusive bar found at bar %i)" % (j, )
                            break
                    count = 0
                    for k in range(j+1, i): # checking for inbetween tops
                        if ind[k] != 0: # top found
                            count += 1
                            print "\t\tinbetween top found at bar %i)" % (k, )
                            if ind[k] in [1, 11, 21, 31]: 
                                pl.remove(k) # removing top indexes from list
                                print "\t\tindex %i removed from previous low list" % (k, )
                            if ind[k] in [2, 12, 22, 32]: 
                                ph.remove(k) # idem
                                print "\t\tindex %i removed from previous high list" % (k, )
                            ind[k] = 0 # reset top
                            print "\t\ttop at bar %i) reset to 0" % (k, )
                    if count > 0:
                        if len(pl) and len(ph):
                            if (pl[-1] > ph[-1]): # if true, low is most recent
                                last_fixed = pl[-1], 1
                                mark = i, 2
                                print "\t\tlast_fixed set to %i, %i; mark set to %i, %i" % (last_fixed[0], last_fixed[1], mark[0], mark[1])
                            elif (ph[-1] > pl[-1]): # high is most recent
                                last_fixed = ph[-1], 2
                                mark = i, 1
                                print "\t\tlast_fixed set to %i, %i; mark set to %i, %i" % (last_fixed[0], last_fixed[1], mark[0], mark[1])
                        elif len(pl) and not len(ph):
                            last_fixed = pl[-1], 1
                            mark = i, 2
                            print "\t\tlast_fixed set to %i, %i; mark set to %i, %i" % (last_fixed[0], last_fixed[1], mark[0], mark[1])
                        elif len(ph) and not len(pl):
                            last_fixed = ph[-1], 2
                            mark = i, 1
                            print "\t\tlast_fixed set to %i, %i; mark set to %i, %i" % (last_fixed[0], last_fixed[1], mark[0], mark[1])
                        elif not len(pl) and not len(ph):
                            last_fixed = None
                            mark = i, 0 # current outside bar has become indifferent
                            print "\t\tlast_fixed set to None; mark set to %i, %i" % mark
                    if count == 0: # no inbetween tops found
                        mark = i, mark[1] # move mark to current outside bar; signal remains the same
                        print "\t\tno inbetween tops found; mark set to %i, %i" % mark
                continue
            if highs[i]  > highs[mark[0]] and lows[i] >= lows[mark[0]]: # upbar
                print "\tupbar"
                if   mark[1]  < 2: # upbar with previous indifferent or low mark
                    print "\t\twith previous indifferent or low mark"
                    if pl == []: 
                        ind[mark[0]] = 1 # L
                        print "\t\tno previous low; bar %i) marked as L (1)" % (mark[0], )
                    else:
                        if    lows[mark[0]]  <   lows[pl[-1]]: 
                            ind[mark[0]] = 11 # LL
                            print "\t\tbar %i) marked as LL (11)" % (mark[0], )
                        elif  lows[mark[0]] ==   lows[pl[-1]]: 
                            ind[mark[0]] = 21 # EL
                            print "\t\tbar %i) marked as EL (21)" % (mark[0], )
                        elif  lows[mark[0]]  >   lows[pl[-1]]: 
                            ind[mark[0]] = 31 # HL
                            print "\t\tbar %i) marked as HL (31)" % (mark[0], )
                    pl.append(mark[0])
                    print "\t\t\t%i append to previous low list" % (mark[0], )
                    last_fixed = mark[0], 1
                    print "\t\t\tlast_fixed changed to %i, %i" % last_fixed
                    mark = i, 2
                    print "\t\t\tmark set to: %i, %i" % mark
                    ind[i] = 0
                    print "\t\t\tcurrent bar %i) marked as no top (0)" % (i, )
                elif mark[1] == 2: # upbar with previous high mark
                    print "\t\twith previous high mark"
                    ind[mark[0]] = 0 # reset previous mark
                    print "\t\tprevious mark in ind on position %i) reset to 0" % (mark[0], )
                    mark = i, 2
                    print "\t\t\tmark set to: %i, %i" % mark
                    ind[i] = 0
                    print "\t\t\tcurrent bar %i) marked as no top (0)" % (i, )
                continue
            if highs[i] <= highs[mark[0]] and lows[i]  < lows[mark[0]]: # downbar
                print "\tdownbar"
                if   mark[1] != 1: # downbar with previous indifferent or high mark
                    print "\t\twith previous indifferent or low mark"
                    if ph == []: 
                        ind[mark[0]] = 2 # H
                        print "\t\tno previous high; bar %i ) marked as H (2)" % (mark[0], )
                    else:
                        if   highs[mark[0]]  < highs[ph[-1]]: 
                            ind[mark[0]] = 12 # LH
                            print "\t\tbar %i) marked as LH (12)" % (mark[0], )
                        elif highs[mark[0]] == highs[ph[-1]]: 
                            ind[mark[0]] = 22 # EH
                            print "\t\tbar %i) marked as EH (22)" % (mark[0], )
                        elif highs[mark[0]]  > highs[ph[-1]]: 
                            ind[mark[0]] = 32 # HH
                            print "\t\tbar %i) marked as HH (32)" % (mark[0], )
                    ph.append(mark[0])
                    print "\t\t\t%i append to previous high list" % (mark[0], )
                    last_fixed = mark[0], 2
                    print "\t\t\tlast_fixed changed to %i, %i" % last_fixed
                    mark = i, 1
                    print "\t\t\tmark set to: %i, %i" % mark
                    ind[i] = 0
                    print "\t\t\tcurrent bar %i) marked as no top (0)" % (i, )
                elif mark[1] == 1: # downbar with previous low mark
                    print "\t\twith previous low mark"
                    ind[mark[0]] = 0 # reset previous mark
                    print "\t\tprevious mark in ind on position %i) reset to 0" % (mark[0], )
                    mark = i, 1
                    print "\t\t\tmark set to: %i, %i" % mark
                    ind[i] = 0
                    print "\t\t\tcurrent bar %i) marked as no top (0)" % (i, )
                continue
        #if ind[mark[0]] == self.empty:
        #    print "\tbar %i) marked as empty" % (mark[0], )
        #    if mark[1] != 1:
        #        print "\t\tmark[1]=%i" % (mark[1], )
        #        if highs[mark[0]]  < highs[ph[-1]]: 
        #            ind[mark[0]] = 12 # LH
        #            print "\t\tbar %i) marked as LH (12)" % (mark[0], )
        #        if highs[mark[0]] == highs[ph[-1]]: 
        #            ind[mark[0]] = 22 # EH
        #            print "\t\tbar %i) marked as EH (22)" % (mark[0], )
        #        if highs[mark[0]]  > highs[ph[-1]]: 
        #            ind[mark[0]] = 32 # HH
        #            print "\t\tbar %i) marked as HH (32)" % (mark[0], )
        #        last_fixed = mark[0], 2
        #        print "\t\t\tlast_fixed changed to %i, %i" % last_fixed
        #    if mark[1]  < 2: # PM change to elif
        #        print "\t\tmark[1]=%i" % (mark[1], )
        #        if  lows[mark[0]]  <   lows[pl[-1]]: 
        #            ind[mark[0]] = 11 # LL
        #            print "\t\tbar %i) marked as LL (11)" % (mark[0], )
        #        if  lows[mark[0]] ==   lows[pl[-1]]: 
        #            ind[mark[0]] = 21 # EL
        #            print "\t\tbar %i) marked as EL (21)" % (mark[0], )
        #        if  lows[mark[0]]  >   lows[pl[-1]]: 
        #            ind[mark[0]] = 31 # HL
        #            print "\t\tbar %i) marked as HL (31)" % (mark[0], )
        #        last_fixed = mark[0], 1
        #        print "\t\t\tlast_fixed changed to %i, %i" % last_fixed
        if ar:
            data[fr] = ind
            return fr
        else: return ind
