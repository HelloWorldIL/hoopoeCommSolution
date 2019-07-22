from hsl_comm import Predict
from skyfield.api import load, Topos
from datetime import datetime, timedelta

sat = load.tle('https://celestrak.com/NORAD/elements/active.txt')['SHAONIAN XING']
station = Topos(latitude='32.1150 N', longitude='34.7820 E', elevation_m=13)
predict = Predict(sat, station)

ts = load.timescale()

t = ts.now()
t1 = ts.utc(t.utc_datetime()+timedelta(days=1))

tDateTime = t.utc_datetime()

passes = predict.getNextPasses(t, t1)

# start = boundaries[1][0]
# end = boundaries[1][1]
# times = predict.getNextPasses(start, end)

for single_pass in passes:
    if single_pass[2] > 1:
        print(single_pass[2])
