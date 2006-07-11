"""Unit test for Ema.py

"""

__author__ = "Sander Smits (jhmsmits@xs4all.nl)"
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2006/07/04 20:54:20 $"
__copyright__ = "Copyright (c) 2006 Sander Smits"
__license__ = "Python"

from ta.Ema import *
import unittest

inputValues = [(datetime.datetime(2006, 5, 1), 12.34, 12.56, 12.11, 12.20, 2010912),
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

class BadInitializationInput(unittest.TestCase):
    def testNoneParameter(self):
        """ initializing should fail with None parameter """
        self.assertRaises(IndicatorError, Ema, None)
        
    def testTupleParameter(self):
        """ initializing should fail with tuple parameter """
        self.assertRaises(IndicatorError, Ema, (4, ))
        
    def testStringParameter(self):
        """ initializing should fail with str parameter """
        self.assertRaises(IndicatorError, Ema, '4')
        
    def testNegativeIntParameter(self):
        """ initializing should fail with negative int parameter """
        self.assertRaises(IndicatorError, Ema, -1)
        
    def testEmptyParameter(self):
        """ initializing should raise TypeError with empty parameter """
        self.assertRaises(TypeError, Ema)
        
class KnownValues(unittest.TestCase):
    def testOutputKnownValues(self):
        """Ema calculation should give known result with known input
           results are rounded by str representation of floats
        """
        s = Ema(4)
        knownvalues = [None, None, None, 12.24, 12.372, 12.3032, 12.26992, 12.225952]
        for c in inputValues[:8]:
            s.append(c)
        for i in range(len(s.output)):
            self.assertEqual(str(s.output[i]), str(knownvalues[i]))