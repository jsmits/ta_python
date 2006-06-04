import logging
import logging.config
import os
import datetime

class Strategy:
    
    NOACTION = 0
    BUY = 1
    SELLSHORT = 2
    SELL = 3
    
    def __init__(self, timeframes = []):

        self.timeframes = timeframes
        
    def handleTick(self, time, last):
        # validation is done in Tradable
        for timeframe in self.timeframes:
            timeframe.handleTick(time, last)
        return self.evaluate()
        
    def evaluate(self):
        if self.buy():
            return self.BUY
        if self.sellShort():
            return self.SELLSHORT
        if self.sell():
            return self.SELL
        return self.NOACTION
        
    def buy(self):
        pass
    
    def sellshort(self):
        pass
    
    def sell(self):
        pass
    
    
    
    