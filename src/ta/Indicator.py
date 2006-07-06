import datetime

class Indicator:
    def __init__(self):
        self.times = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
        
        self.input = []
        self.output = []
        
# define exceptions
class IndicatorError(Exception): pass
class NotTupleError(IndicatorError): pass
class NotFloatError(IndicatorError): pass
class InvalidCandleStickError(IndicatorError): pass
class InvalidDateTimeError(IndicatorError): pass

def validateInput(value, times):
    if type(value) is not tuple:
        raise NotTupleError, 'invalid input: should be a tuple (d, o, h, l, c, v); input: %s' % (value,)
    if len(value) != 6:
        raise InvalidCandleStickError, 'invalid input: tuple length should be 6; input: %s' % (value,)
    if not type(value[0]) is datetime.datetime:
        raise InvalidDateTimeError, 'invalid input: tuple element [0] should be a datetime; input: %s' % (value[0],)
    for i in range(1,5):
        if type(value[i]) is not int and type(value[i]) is not float:
            raise InvalidCandleStickError, 'invalid input: tuple element [%s] is not int or float; input: %s' % (i,value[i])
    if len(times) > 0 and value[0] < times[-1]:
        raise InvalidDateTimeError, 'invalid input: tuple element [0] (datetime) should be equal or greater than previous: %s; input: %s' % (times[-1], value[0])  
    if type(value[5]) is not int:
        raise InvalidCandleStickError, 'invalid input: volume should be int; input: %s' % value[5]
