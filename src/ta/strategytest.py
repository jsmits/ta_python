from Strategy import Strategy
from TimeFrame import *
from Tops import *
from DBConnector import TAdb
import datetime
import random

tf3 = TimeFrame(3, indicators=[Tops(signals=['ALHHHL'])])
tf20 = TimeFrame(20, indicators=[Tops(signals=['ALHHHL'])])

s = Strategy(timeframes=[tf3, tf20])
ta = TAdb()
tickdata = ta.exampleTickData(10000)

nrofticks = len(tickdata)
start = datetime.datetime.now()
for d, close in tickdata:
    s.handleTick(d, close)
    if s.actionType() == Strategy.BUY:
        print "BUY action after tick with time %s and value %s" % (d, close)
end = datetime.datetime.now()
diff = end - start
dfsec = float("" + str(diff.seconds) + "." + str(diff.microseconds))
print "Inserting %s ticks in Strategy with two timeframes took %s seconds. %s candles per second." % (nrofticks, dfsec, nrofticks / dfsec)
tops3 = s.timeframes[0].indicators[0]
print len(tops3.output), len(tops3.times)
