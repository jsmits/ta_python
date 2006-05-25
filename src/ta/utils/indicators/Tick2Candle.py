import logging
import logging.config
import os
import datetime
import time

class Tick2Candle:
    
    def __init__(self, period):
        self.period = period
        
        self.logger = logging.getLogger(self.__class__.__name__)
        try: logging.config.fileConfig(os.getcwd() + "/logging.conf")
        except: logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', filename=self.__class__.__name__+'.log', filemode='w')
        
        self.inputtimes = [] # tick times
        self.starttime = None
        self.endtime = None
        self.last = [] # tick values

        self.time = None
        self.open = None
        self.high = None
        self.low = None
        self.close = None
        
        self.returnvalue = None
        
    def processTick(self, time, value):
        
        if not self.starttime: # first time
            self.setTimes(time)
        if time < self.endtime: # current candle
            self.inputtimes.append(time)
            self.last.append(value)
            self.createReturnValue(None)
        else: # new candle
            self.createReturnValue(time)
            self.resetAll()
            self.inputtimes.append(time)
            self.last.append(value)
            self.setTimes(time)
            # now append the new virtual candle
            self.returnValue.append((self.starttime, self.last[0], self.last[0], self.last[0], self.last[0], 0))
        return self.returnValue
    
    def setTimes(self, t):
        timestamp = time.mktime(t.timetuple())
        starttimestamp = timestamp - (timestamp % (self.period * 60))
        endtimestamp = starttimestamp + (self.period * 60)
        self.starttime = datetime.datetime.fromtimestamp(starttimestamp)
        self.endtime = datetime.datetime.fromtimestamp(endtimestamp)
                
    def createReturnValue(self, time):
        self.time = self.starttime
        self.open = self.last[0]
        self.high = max(self.last)
        self.low = min(self.last)
        self.close = self.last[-1]
        if not time:
            self.returnValue = []
            self.returnValue.append((self.time, self.open, self.high, self.low, self.close, 0))
        else:
            self.returnValue = []
            self.returnValue.append((self.time, self.open, self.high, self.low, self.close, 0))
            # check for gap
            self.returnValue += self.gapValues(time)
            
        
    def gapValues(self, t):
        newtimestamp = time.mktime(t.timetuple())
        endtimestamp = time.mktime(self.endtime.timetuple())
        delta = newtimestamp - endtimestamp
        gaps = int(delta / (self.period * 60))
        gapList = []
        for i in range(gaps):
            gapList.append((self.endtime + datetime.timedelta(0, (i * self.period * 60)), self.close, self.close, self.close, self.close, 0))
        return gapList
    
    def resetAll(self):
        self.inputtimes = []
        self.last = []
        
        self.time = None
        self.open = None
        self.high = None
        self.low = None
        self.close = None
    
if __name__=='__main__':
    tc = Tick2Candle(3)
    
    ticks = [(datetime.datetime(2006,12,5,9,30,0), 12.55),
             (datetime.datetime(2006,12,5,9,30,15), 13.02),
             (datetime.datetime(2006,12,5,9,30,30), 12.53),
             (datetime.datetime(2006,12,5,9,30,45), 13.04),
             (datetime.datetime(2006,12,5,9,31,5), 13.08),
             (datetime.datetime(2006,12,5,9,34,15), 13.28),
             (datetime.datetime(2006,12,5,9,34,30), 13.05),
             (datetime.datetime(2006,12,5,9,34,35), 13.02),
             (datetime.datetime(2006,12,5,9,34,43), 12.53),
             (datetime.datetime(2006,12,5,9,35,45), 13.04),
             (datetime.datetime(2006,12,5,9,36,5), 13.08),
             (datetime.datetime(2006,12,5,9,38,15), 13.28)]
    
    start = datetime.datetime.now()
    for t in ticks:
        print tc.processTick(t[0], t[1])
    end = datetime.datetime.now()
    diff = end - start
    dfsec = float("" + str(diff.seconds) + "." + str(diff.microseconds))
    print "Processing %s ticks took %s seconds." % (len(ticks), dfsec)