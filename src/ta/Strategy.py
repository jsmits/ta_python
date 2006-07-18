import logging
import logging.config
import os
import datetime

class Strategy:
    
    NOACTION = 0
    BUY = 1
    SELLSHORT = 2
    SELL = 3
    
    def __init__(self, timeframes = [], action=BUY):

        self.timeframes = timeframes
        self.action = action
        
    def handleTick(self, time, last):
        # validation is done in Tradable
        for timeframe in self.timeframes:
            timeframe.handleTick(time, last)
        
    def actionType(self):
        if not self.timeframes: return self.NOACTION
        for timeframe in self.timeframes:
            if not timeframe.indicators: return self.NOACTION
            for indicator in timeframe.indicators:
                if indicator.signal() == False: return self.NOACTION
                elif indicator.signal() != True:
                    raise Exception, 'indicator signal should always be True or False; signal %s' % indicator.signal
        return self.action
    
    
    
    