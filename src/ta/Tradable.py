import logging
import logging.config
import os
import datetime
from Strategy import *

class Tradable:
    
    def __init__(self, id=None, symbol='', type=None, *args, **kwargs):
        
        self.id = id
        self.symbol = symbol
        self.type = type
        
        self.name = '' # TODO
        self.description = '' # TODO
        
        self.exchange = '' # TODO
        
        self.timezone # TODO
        self.openingtime = None # TODO (in timezone)
        self.closingtime = None # TODO (in timezone)
        
        self.strategies = [] # to be filled with strategy objects
        
        self.logger = logging.getLogger(self.__class__.__name__)
        try: logging.config.fileConfig(os.getcwd() + "/logging.conf")
        except: logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', filename=self.__class__.__name__+'.log', filemode='w')
    
    def handleTick(self, time, last):
        if not self._validateTick(time, last):
            # raise Error
            return
        for strategy in self.strategies: # pass the tick to the strategies
            strategy.handleTick(time, last)
            action = strategy.actionType()
            self.handleAction(action)
        
    def _validateTick(self, time, last):
        if not time:
            self.logger.error('invalid input: time is not supplied') 
            return False
        if not last:
            self.logger.error('invalid input: last is not supplied') 
            return False
        if not type(time) is datetime.datetime:
            self.logger.error('invalid input: time should be a datetime; input: %s' % (time,)) 
            return False
        if not (type(last) is int or type(last) is float):
            self.logger.error('invalid input: last should be an int or float; input: %s' % (last,)) 
            return False    
        return True
    
    def handleAction(self, action):
        if action == Strategy.NOACTION:
            pass
        if action == Strategy.BUY:
            # check if we can send out a buy
            # build an order dictionary and send it to the orderlistener
            # e.g. {'id' : self.id, 'action' : action, 'price' : last, 'time' : time, 'number' : 200}
            # if ok, update the orderstatus object
            pass
        if action == Strategy.SELLSHORT:
            pass
        if action == Strategy.SELL:
            pass
        
        