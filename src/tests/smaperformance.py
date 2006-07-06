from ta.Sma import *
import datetime
import random

ind = Sma(3)

d = datetime.datetime(2005, 1, 1, 9, 30)
td = datetime.timedelta(0, 1)
close = 12.20
nrofticks = int(60 * 60 * 6.5) # one market day with one tick every second
start = datetime.datetime.now()
for x in xrange(nrofticks):
    c = (d, 12.34, 12.56, 12.11, close, 20192812)
    ind.append(c)
    d = d + td
    if (random.random() > 0.4): close = close + random.random()/2
    else: close = close - random.random()/2
end = datetime.datetime.now()
diff = end - start
logger.debug(ind)
dfsec = float("" + str(diff.seconds) + "." + str(diff.microseconds))
logger.info("Inserting %s candles took %s seconds. %s candles per second." % (nrofticks, dfsec, nrofticks / dfsec))