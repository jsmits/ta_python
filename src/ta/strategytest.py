from Strategy import Strategy
from TimeFrame import *
from Tops import *
from DBConnector import TAdb
import datetime
import random

tf3 = TimeFrame(3, indicators=[Tops(signals=['ALHHHL']), Sma(13, signals=['crossoverup'])])
tf20 = TimeFrame(20, indicators=[Sma(4, signals=['crossoverup'])])

s = Strategy(timeframes=[tf3, tf20])
ta = TAdb()
tickdata = ta.exampleTickData()[:800]

#d = datetime.datetime(2005, 1, 1, 15, 30)
#td = datetime.timedelta(0, 1)
#close = 12.20
#nrofticks = int(60 * 60 * 6.5) # one market day with one tick every second
nrofticks = len(tickdata)
start = datetime.datetime.now()
#for x in xrange(nrofticks):
for d, close in tickdata:
    s.handleTick(d, close)
#    d = d + td
#    if (random.random() > 0.4): close = close + random.random()/2
#    else: close = close - random.random()/2
end = datetime.datetime.now()
diff = end - start
dfsec = float("" + str(diff.seconds) + "." + str(diff.microseconds))
print "Inserting %s ticks in Strategy with two timeframes took %s seconds. %s candles per second." % (nrofticks, dfsec, nrofticks / dfsec)
tops3 = s.timeframes[0].indicators[0]
print len(tops3.output), len(tops3.times)
print tops3.report