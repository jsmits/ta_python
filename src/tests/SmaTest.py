import os
import sys

sys.path.append( os.getcwd() )

from indicators.Sma import *

s = Sma(4)
print s