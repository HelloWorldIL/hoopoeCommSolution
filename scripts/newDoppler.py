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
import subprocess


args = ArgumentParser()
args.add_argument("--config", type=str, help="Configuration file path",
                  default=os.environ['HOME']+"/.hslCommSolution/config.ini")

config = ConfigParser()
config.read(args.parse_args().config)

# Station prams
stationlat = config['Ground Station']['lat']
stationlon = config['Ground Station']['lon']
stationAlt = int(config['Ground Station']['alt'])

# TLE and sat params
tleURL = config['TLE']['url']
satName = config['TLE']['sat']
F0 = int(config['Doppler']['freq'])  # Center Frequency

sat = load.tle(tleURL)[satName]
station = Topos(stationlat, stationlon, elevation_m=stationAlt)

# Network params
dopplerPort = config['Doppler']['port']
rotatorPort = config['Rotator']['port']

# Rotator params
rotatorModel = config['Rotator']['model']
rotatorDevice = config['Rotator']['device']


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
        print("Send failed, is the host running?")


def sendRotatorTCP(tn, az, el):
    try:
        tn.write(("P " + str(az) + ", " + str(az)).encode("ascii"))
    except socket.error:
        print("Send failed, is the host running?")


def connectDoppler(host, port):
    try:
        return Telnet(host, port)
    except socket.error:
        print("Connection refused, is the host running?")


def connectRotator(model, device):
    proc = subprocess.Popen(f'rotctl --model={model} --rot-file={device}', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()
    if proc.returncode != 0:
        print("Error connecting to rotator")
    return proc


def main():
    tn = connectDoppler("localhost", dopplerPort)
    tnRot = connectDoppler("localhost", rotatorPort)
    while True:
        t = load.timescale().utc(datetime.utcnow().replace(tzinfo=utc))
        el, az, dist = altAzCalc(sat, station, t)
        doppler = dopplerCalc(sat, station, t, F0)
        print("Azimuth: " + str(int(az._degrees)))
        print("Elevation: " + str(int(el.degrees)))
        print("Frequency: " + str(doppler))
        sendDoppler(tn, doppler)
        sendRotatorTCP(tnRot, int(az.degrees), int(el.degrees))
        time.sleep(0.2)


def sendRotator(proc, az, el):
    toSend = f'P {az} {el}'
    if int(el) > 0:
        return proc.communicate(input=toSend.encode())
    print("Satellite is not over the horizon!")


print(f'rotctl --model={rotatorModel} --rot-file={rotatorDevice}')

rotctlProc = connectRotator(rotatorModel, rotatorDevice)

#out, err = sendRotator(rotctlProc, str(5), str(10))
rotctlProc.kill()