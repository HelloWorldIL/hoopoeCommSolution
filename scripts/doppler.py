#!/usr/bin/env python3

import ephem
import socket
import sys
import os
import time
from time import gmtime, strftime
import argparse
import telnetlib

def main():
    # Define parser arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--freq", type=int, help="Satellite center freq (Default=437.73Mhz)", default=437730000)
    parser.add_argument("--lat", type=str, help="Ground station Latitude (Default=32.1150)", default='32.1150')
    parser.add_argument("--lon", type=str, help="Ground station Latitude (Default=34.7820)", default='34.7820')
    parser.add_argument("--alt", type=int, help="Ground station Altitude in meters above sea level (Default=13)", default=13)
    parser.add_argument("--tle", type=str, help="TLE file location", default=os.environ['HOME'] + '/tlefile.tle')
    parser.add_argument("--sat", type=str, help="Satellite name (Default=HOOPOE)", default='HOOPOE')
    parser.add_argument("--port", type=int, help="Host port (Default=7356)", default=7356)
    parser.add_argument("--debug", type=bool, help="Debug? Prints Errors and data (Default=False)", default=False)

    # Variables
    C = 299792458.
    F0 = parser.parse_args().freq
    LATITUDE = parser.parse_args().lat
    LONGITUDE = parser.parse_args().lon
    ALTITUDE = parser.parse_args().alt
    TLEFILE = parser.parse_args().tle
    SATNAME = parser.parse_args().sat
    PORT = parser.parse_args().port
    DEBUG = parser.parse_args().debug

    # Open tle file
    with open(TLEFILE, 'r') as f:
        data = f.readlines()

    # Define an observer
    QSO = ephem.Observer()
    QSO.lon = LONGITUDE
    QSO.lon = LATITUDE
    QSO.elevation = ALTITUDE

    # Find sat tle and define a sat
    for i in range(len(data)):
        if SATNAME in data[i]:
            sat = ephem.readtle(data[i], data[i+1], data[i+2])

    # Dopler calculation
    def dopplercalc():
        QSO.date = strftime('%Y/%m/%d %H:%M:%S', gmtime())
        sat.compute(QSO)
        doppler = int(F0 - sat.range_velocity * F0 / C)
        return doppler

    # Main loop
    closed = False
    try:
        tn = telnetlib.Telnet("localhost", PORT)
        if DEBUG: 
            print ("Started doppler script for " + SATNAME + " Sending commands to port " + str(PORT) + " \n")
        closed = True
        while True:
            if DEBUG: 
                print (dopplercalc())
            tn.write("F " + str(dopplercalc()))
            time.sleep(1)
    except (socket.error):
        if DEBUG:
            if not closed:
                print ("Connection refused, is the host running?")
            else:
                print ("Connection closed.")
        

# Catch keyboard interrupt
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
