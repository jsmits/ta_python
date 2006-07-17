from ta.Strategy import Strategy
from ta.TimeFrame import *
from ta.Tops import *
import datetime
import random

tf3 = TimeFrame(3, indicators=[Tops(signals=['ALHHHL'])])
tf20 = TimeFrame(20, indicators=[Tops(signals=['LLLHHL'])])

s = Strategy(timeframes=[tf3, tf20])

d = datetime.datetime(2005, 1, 1, 9, 30)
td = datetime.timedelta(0, 1)
close = 12.20
nrofticks = int(60 * 60 * 6.5) # one market day with one tick every second
start = datetime.datetime.now()
for x in xrange(nrofticks):
    s.handleTick(d, close)
    d = d + td
    if (random.random() > 0.4): close = close + random.random()/2
    else: close = close - random.random()/2
end = datetime.datetime.now()
diff = end - start
dfsec = float("" + str(diff.seconds) + "." + str(diff.microseconds))
print "Inserting %s ticks in Strategy with two timeframes took %s seconds. %s candles per second." % (nrofticks, dfsec, nrofticks / dfsec)
