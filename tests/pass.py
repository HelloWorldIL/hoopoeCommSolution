from hsl_comm import Predict
from skyfield.api import load, Topos
from datetime import datetime, timedelta

sat = load.tle('https://celestrak.com/NORAD/elements/active.txt')['SHAONIAN XING']
station = Topos(latitude='32.1150 N', longitude='34.7820 E', elevation_m=13)
predict = Predict(sat, station)

ts = load.timescale()

t = ts.now()
t1 = ts.utc(t.utc_datetime()+timedelta(days=5))

tDateTime = t.utc_datetime()

times = predict.getNextPasses(t, t1)

print(times[0])