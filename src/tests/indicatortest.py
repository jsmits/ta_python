"""Unit test for Indicator.py

"""

__author__ = "Sander Smits (jhmsmits@xs4all.nl)"
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2006/07/04 20:54:20 $"
__copyright__ = "Copyright (c) 2006 Sander Smits"
__license__ = "Python"

from ta.Indicator import *
import unittest

class AppendBadCandle(unittest.TestCase):
    def testInteger(self):
        """append should fail with integer input"""
        s = Indicator(None)
        self.assertRaises(NotTupleError, s.append, 4000)
        
    def testString(self):
        """append should fail with string input"""
        s = Indicator(None)
        self.assertRaises(NotTupleError, s.append, "dummy")
        
    def testFloat(self):
        """append should fail with float input"""
        s = Indicator(None)
        self.assertRaises(NotTupleError, s.append, 12.432)
        
    def testFloatVolume(self):
        """append should fail with float value for volume"""
        s = Indicator(None)
        c = (datetime.datetime(2006, 5, 19), 12.34, 12.56, 12.11, 12.20, 2010912.25)
        self.assertRaises(InvalidCandleStickError, s.append, c)
     
    def testStringOpen(self):
        """append should fail with string value for open"""
        s = Indicator(None)
        c = (datetime.datetime(2006, 5, 19), "dummy", 12.56, 12.11, 12.20, 2010912)
        self.assertRaises(InvalidCandleStickError, s.append, c)
    
    def testNoneOpen(self):
        """append should fail with None value for open"""
        s = Indicator(None)
        c = (datetime.datetime(2006, 5, 19), None, 12.56, 12.11, 12.20, 2010912)
        self.assertRaises(InvalidCandleStickError, s.append, c)
        
    def testTupleTooLarge(self):
        """append should fail with tuple that has a length bigger than 6"""
        s = Indicator(None)
        c = (datetime.datetime(2006, 5, 19), None, 12.56, 12.11, 12.20, 2010912, 1425)
        self.assertRaises(InvalidCandleStickError, s.append, c)
        
    def testTupleTooSmall(self):
        """append should fail with tuple that has a length smaller than 6"""
        s = Indicator(None)
        c = (datetime.datetime(2006, 5, 19), None, 12.56, 12.11, 12.20)
        self.assertRaises(InvalidCandleStickError, s.append, c)
        
    def testOlderDateTime(self):
        """append should fail with candle input that has an older datetime than the most recently processed candle """
        s = Indicator(None)
        inputValues = [(datetime.datetime(2006, 5, 1), 12.34, 12.56, 12.11, 12.20, 2010912),
                       (datetime.datetime(2006, 5, 2), 12.24, 12.48, 12.20, 12.22, 8791029),
                       (datetime.datetime(2006, 5, 3), 12.18, 12.20, 11.88, 12.16, 5434255),
                       (datetime.datetime(2006, 5, 4), 12.24, 12.68, 12.24, 12.38, 8734251)]
        for c in inputValues:
            s.append(c)
        self.assertRaises(InvalidDateTimeError, s.append, inputValues[2])
        
    def testIntegerDateTime(self):
        """append should fail with candle input that does not have a datetime as first element """
        s = Indicator(None)
        c = (1562516271, 12.34, 12.56, 12.11, 12.20, 2010912)
        self.assertRaises(InvalidDateTimeError, s.append, c)
        
    def testNegativeLow(self):
        """append should fail with negative low value"""
        s = Indicator(None)
        c = (datetime.datetime(2006, 5, 19), 12.34, 12.56, -12.11, 12.20, 2010912)
        self.assertRaises(InvalidCandleStickError, s.append, c)
        
    def testHighLowMixUp(self):
        """append should fail with high lower than low"""
        s = Indicator(None)
        c = (datetime.datetime(2006, 5, 19), 12.34, 12.11, 12.56, 12.20, 2010912)
        self.assertRaises(InvalidCandleStickError, s.append, c)
        
    def testOpenHigherThanHigh(self):
        """append should fail with open higher than high"""
        s = Indicator(None)
        c = (datetime.datetime(2006, 5, 19), 12.60, 12.56, 12.11, 12.20, 2010912)
        self.assertRaises(InvalidCandleStickError, s.append, c)
    
    def testCloseLowerThanLow(self):
        """append should fail with close lower than low"""
        s = Indicator(None)
        c = (datetime.datetime(2006, 5, 19), 12.60, 12.56, 12.11, 12.09, 2010912)
        self.assertRaises(InvalidCandleStickError, s.append, c)
