import os
import sys

from ta.Sma import *
import ta.Logger

logger = ta.Logger.logger()

s = Sma(4)
print s

logger.info("sma test logging")