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


class SatPredictUtills(object):
    def __init__(self, sat, station, F0):
        self.sat = sat
        self.station = station
        self.F0 = F0

    def getDopplerFreq(self, t):
        C = 299792458
        t1 = load.timescale().utc(t.utc_datetime()+timedelta(seconds=1))

        diff = (self.sat - self.station).at(t)
        diff1 = (self.sat - self.station).at(t1)

        range1 = diff.distance().km
        range2 = diff1.distance().km
        change = (range1 - range2)*1000

        return int((self.F0 * (C + change) / C))
    
    def getAzEl(self, parameter_list):
        diff = (self.sat - self.station).at(t)
        return (diff.altaz()[1].degrees, diff.altaz()[0].degrees)


def getConfig(configLocation=os.environ['HOME']+"/.hslCommSolution/config.ini"):
    config = ConfigParser()
    config.read(configLocation)

    # Station prams
    stationlat = config['Ground Station']['lat']
    stationlon = config['Ground Station']['lon']
    stationAlt = int(config['Ground Station']['alt'])

    # TLE and sat params
    tleURL = config['TLE']['url']
    satName = config['TLE']['sat']
    F0 = int(config['Doppler']['freq'])  # Center Frequency

    # Network params
    dopplerPort = config['Doppler']['port']
    # Rotator params
    rotatorModel = config['Rotator']['model']
    rotatorDevice = config['Rotator']['device']

    return {
        "station": {
            "stationLat": stationlat,
            "stationLon": stationlon,
            "stationAlt": stationAlt,
        },
        "satellite": {
            "satName": satName,
            "F0": F0,
        },
        "dopplerPort": dopplerPort,
        "rotator": {
            "model": rotatorModel,
            "device": rotatorDevice,
        },
        "tleURL": tleURL,
    }


class SatPredict(object):
    def __init__(self, configLocation=os.environ['HOME']+"/.hslCommSolution/config.ini"):
        if os.path.isfile(configLocation):
            self.__getConfig(configLocation=configLocation)
            self.sat = load.tle(self.tleURL)[self.satName]
            self.station = Topos(
                self.stationlat, self.stationlon, elevation_m=self.stationAlt)
            self.__satUtills = SatPredictUtills(
                self.sat, self.station, self.F0)
            self.dopplerConnection = None
            self.rotatorProc = None
        else:
            raise Exception("Config file not found")

    def getDopplerFreq(self, t):
        return self.__satUtills.getDopplerFreq(t)

    def getAzEl(self, t):
        return self.__satUtills.getAzEl(t)

    def __connectDoppler(self):
        self.dopplerConnection = Telnet("localhost", self.dopplerPort)

    def sendDoppler(self, t):
        toWrite = "F " + str(self.getDopplerFreq(t)) + "\n"
        if self.dopplerConnection is None:
            try:
                self.__connectDoppler()
            except socket.error:
                print("Connection error, is the host running?")
        try:
            self.dopplerConnection.write(toWrite.encode("ascii"))
        except socket.error:
            print("Doppler Write Error, is the host running?")
        except AttributeError:
            pass

    def __getConfig(self, configLocation=False):
        config = ConfigParser()
        config.read(configLocation)

        # Station prams
        self.stationlat = config['Ground Station']['lat']
        self.stationlon = config['Ground Station']['lon']
        self.stationAlt = int(config['Ground Station']['alt'])

        # TLE and sat params
        self.tleURL = config['TLE']['url']
        self.satName = config['TLE']['sat']
        self.F0 = int(config['Doppler']['freq'])  # Center Frequency

        # Network params
        self.dopplerPort = config['Doppler']['port']
        # Rotator params
        self.rotatorModel = config['Rotator']['model']
        self.rotatorDevice = config['Rotator']['device']

    def __connectRotator(self):
        proc = subprocess.Popen('rotctl --model={self.rotatorModel} --rot-file={self.rotatorDevice}', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.communicate()
        if proc.returncode is not 0:
            raise Exception("Error connecting to rotator")
        self.rotatorProc = subprocess.Popen('rotctl --model={self.rotatorModel} --rot-file={self.rotatorDevice}', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def sendRotator(self, t):
        if self.rotatorProc is None:
            self.__connectRotator()

        azimuth, elevation = self.getAzEl(t)
        if (elevation > 0):
            toSend = f'P {azimuth} {elevation}\n'
            self.rotatorProc.stdin.write(toSend.encode())
            self.rotatorProc.stdin.flush()
        else:
            print("Satellite is not over the horizon")

predict = SatPredict()
while True:
    t = load.timescale().utc(datetime.utcnow().replace(tzinfo=utc))
    print(predict.getAzEl(t))
    time.sleep(1)
