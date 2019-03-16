#!/usr/bin/env python3
from skyfield.api import Topos, load, utc
from datetime import date, time, datetime
from argparse import ArgumentParser
from configparser import ConfigParser
import os

args = ArgumentParser()
args.add_argument("--config", type=str, help="Configuration file path", default=os.environ['HOME']+"/.hslCommSolution/config.ini")

config = ConfigParser()
config.read(args.parse_args().config)


sat = load.tle(config['TLE']['url'])[config['TLE']['sat']]
station = Topos(config['Ground Station']['lat'], config['Ground Station']['lon'])

t = load.timescale().utc(datetime.now().replace(tzinfo=utc))

diff = (sat-station).at(t)

# TODO Add doppler and rotator correction