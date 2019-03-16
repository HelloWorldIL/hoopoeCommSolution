#!/usr/bin/env python3
from skyfield.api import Topos, load, utc
from skyfield.sgp4lib import EarthSatellite
import socket
import time
import numpy as np
from datetime import datetime, timedelta
from argparse import ArgumentParser
from configparser import ConfigParser
import os
from telnetlib import Telnet


args = ArgumentParser()
args.add_argument("--config", type=str, help="Configuration file path",
                  default=os.environ['HOME']+"/.hslCommSolution/config.ini")

config = ConfigParser()
config.read(args.parse_args().config)

sat = load.tle(config['TLE']['url'])[config['TLE']['sat']]
station = Topos(config['Ground Station']['lat'], config['Ground Station']
                ['lon'], elevation_m=int(config['Ground Station']['alt']))

F0 = int(config['Doppler']['freq'])


def dopplerCalc(sat, station, t, F0):
    t1 = load.timescale().utc(t.utc_datetime()+timedelta(seconds=1))
    C = 299792458

    diff = (sat - station).at(t)
    diff1 = (sat - station).at(t1)
    velocity_magnitude = diff.distance().km
    velocity_magnitude1 = diff1.distance().km
    change = (velocity_magnitude-velocity_magnitude1)*1000
    return int((F0 * (C + change) / (C)))

def altAzCalc(sat, station, t):
    diff = (sat - station).at(t)
    return (diff.altaz())

def sendDoppler(tn, doppler):
    try:
        tn.write(("F " + str(doppler)).encode("ascii"))
    except socket.error:
        print("Connection refused, is the host running?")


# tn = Telnet("localhost", config['Doppler']['port'])
while True:
    t = load.timescale().utc(datetime.utcnow().replace(tzinfo=utc))
    el, az, dist = altAzCalc(sat, station, t)
    doppler = dopplerCalc(sat, station, t, F0)
    print("Azimuth: " + str(int(az._degrees)))
    print("Elevation: " + str(int(el.degrees)))
    print("Frequency: " + str(doppler))
    # sendDoppler(tn, doppler)
    time.sleep(0.2)
