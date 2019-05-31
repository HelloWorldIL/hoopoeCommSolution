from configparser import ConfigParser
import os


class Config(object):
    '''
    The Confic object contains the configuration from the config file

    Args:
        satelliteConfig (SatelliteConfig): A satellite configuration object
        stationConfig (StationConfig): A station configuration object
        dopplerConfic (DopplerConfig): A doppler configuration object
        tleUrl (string): TLE URL
    '''

    def __init__(self, satelliteConfig, stationConfig, dopplerConfic, rotatorConfig, tleUrl):
        self.Satellite = satelliteConfig
        self.Station = stationConfig
        self.Doppler = dopplerConfic
        self.Rotator = rotatorConfig
        self.tleUrl = tleUrl

    @classmethod
    def from_file(cls, config_file=os.path.expanduser('~')+'/.hslCommSolution/config.ini'):
        configParser = ConfigParser()
        configParser.read(config_file)

        satellite = SatelliteConfig(
            configParser.get('Satellite', 'name'),
            configParser.getint('Satellite', 'rxFreq'),
            configParser.getint('Satellite', 'txFreq')
        )
        station = StationConfig(
            configParser.get('Ground Station', 'lat'),
            configParser.get('Ground Station', 'lon'),
            configParser.getint('Ground Station', 'alt')
        )
        doppler = DopplerConfig(
            configParser.get('Doppler', 'rxPort'),
            configParser.get('Doppler', 'txPort')
        )
        rotator = RotatorConfig(
            configParser.get('Rotator', 'model'),
            configParser.get('Rotator', 'device')
        )
        tleUrl = configParser.get('TLE', 'url')
        return cls(
            satellite,
            station,
            doppler,
            rotator,
            tleUrl
        )


class SatelliteConfig(object):
    def __init__(self, name, rxFreq, txFreq):
        self.name = name
        self.rxFreq = rxFreq
        self.txFreq = txFreq

class StationConfig(object):
    def __init__(self, lat, lon, alt):
        self.lat = lat
        self.lon = lon
        self.alt = alt

class DopplerConfig(object):
    def __init__(self, rxPort, txPort=None):
        self.rxPort = rxPort
        self.txPort = txPort

class RotatorConfig(object):
    def __init__(self, model, device):
        self.model = model
        self.device = device