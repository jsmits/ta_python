import os
import sys

from ta.Sma import *
import ta.Logger

logger = Logger.logger()

s = Sma(4)
print s

logger.debug("sma test logging")