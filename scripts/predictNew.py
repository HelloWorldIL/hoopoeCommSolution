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


class Predict(object):
    def __init__(self, sat, station):
        self.sat = sat
        self.station = station

    def getDopplerFreq(self, freq, t):
        C = 299792458
        t1 = load.timescale().utc(t.utc_datetime()+timedelta(seconds=1))

        diff = (self.sat - self.station).at(t)
        diff1 = (self.sat - self.station).at(t1)

        range1 = diff.distance().km
        range2 = diff1.distance().km
        change = (range1 - range2)*1000

        return int((freq * (C + change) / C))

    def getAzEl(self, t):
        diff = (self.sat - self.station).at(t)
        return (diff.altaz()[1].degrees, diff.altaz()[0].degrees)


class DopplerController(object):
    def __init__(self, port):
        self.port = port
        self.connection = None

    def Connect(self):
        if self.connection is None:
            self.connection = Telnet("localhost", self.port)
        else:
            print("Already connected")

    def Write(self, freq):
        toWrite = "F " + str(freq)
        if self.connection is None:
            self.Connect()
        self.connection.write(toWrite.encode("ascii"))


class RotatorController(object):
    def __init__(self, model, device):
        self.model = model
        self.device = device
        self.proc = None

    def Connect(self):
        proc = subprocess.Popen(f'sudo rotctl --model={self.model} --rot-file={self.device}',
                                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.communicate()
        if proc.returncode is not 0:
            raise Exception("Error connecting to rotator")
        self.proc = subprocess.Popen(f'sudo rotctl --model={self.model} --rot-file={self.device}',
                                     shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def Send(self, azimuth, elevation):
        if self.proc is None:
            self.Connect()
        if elevation > 0:
            toSend = f'P {str(azimuth)} {str(azimuth)}\n'
            self.proc.stdin.write(toSend.encode())
            self.proc.stdin.flush()
        else:
            print("Satellite is not over the horizon!")

    def Close(self):
        self.proc.communicate()


class PredictSolution(object):
    def __init__(self, config=os.path.expanduser('~')+'/.hslCommSolution/config.ini'):
        self.__getConfig(config)
        self.sat = load.tle(self.tleURL)[self.satName]
        self.station = Topos(self.stationlat, self.stationlon,
                             elevation_m=self.stationAlt)
        self.dopplerControllerRX = DopplerController(self.rxPort)
        if self.txPort is not None:
            self.dopplerControllerTX = DopplerController(self.txPort)
        else:
            self.dopplerControllerTX = None
        self.rotatorController = RotatorController(
            self.rotatorModel, self.rotatorDevice)
        self.isConnected = False

        self.predict = Predict(self.sat, self.station)

    def __getConfig(self, configLocation):
        config = ConfigParser()
        config.read(configLocation)

        # Station prams
        self.stationlat = config.get('Ground Station', 'lat')
        self.stationlon = config.get('Ground Station', 'lon')
        self.stationAlt = config.getint('Ground Station', 'alt')

        # TLE and sat params
        self.tleURL = config.get('TLE', 'url')
        self.satName = config.get('TLE', 'sat')
        self.txFreq = config.getint('Doppler', 'txFreq', fallback=None)
        self.rxFreq = config.getint('Doppler', 'rxFreq')

        # Network params
        self.rxPort = config.getint('Doppler', 'rxPort')
        self.txPort = config.getint('Doppler', 'txPort')
        # Rotator params
        self.rotatorModel = config.get('Rotator', 'model')
        self.rotatorDevice = config.get('Rotator', 'device')

    def Connect(self):
        self.dopplerControllerRX.Connect()
        if self.dopplerControllerTX is not None:
            self.dopplerControllerTX.Connect()
        self.rotatorController.Connect()
        self.isConnected = True

    def sendDoppler(self, t):
        self.dopplerControllerRX.Write(
            self.predict.getDopplerFreq(self.rxFreq, t))
        if self.dopplerControllerTX is not None:
            self.dopplerControllerTX.Write(
                self.predict.getDopplerFreq(self.txFreq, t)
            )
        self.rotatorController.Send(
            self.predict.getAzEl(t)[0],
            self.predict.getAzEl(t)[1]
        )

    def Start(self):
        if not self.isConnected:
            self.Connect()
        while True:
            t = load.timescale().utc(datetime.utcnow().replace(tzinfo=utc))
            self.sendDoppler(t)
            time.sleep(1)

solution = PredictSolution()
solution.Start()
