from hsl_comm import Predict
from skyfield.api import load, Topos
from datetime import datetime, timedelta

sat = load.tle('https://celestrak.com/NORAD/elements/active.txt')['DUCHIFAT-3']
station = Topos(latitude='32.1150 N', longitude='34.7820 E', elevation_m=13)
predict = Predict(sat, station)
ts = predict.timescale

t = ts.now()
t1 = ts.utc(t.utc_datetime()+timedelta(days=1))

tDateTime = t.utc_datetime()

passes = predict.getNextPasses(t, t1)

print(passes[0])
