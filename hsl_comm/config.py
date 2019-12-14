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

    def __init__(self, satelliteConfig, stationConfig, dopplerConfic, rotatorConfig, sdrConfig, tleUrl):
        self.Satellite = satelliteConfig
        self.Station = stationConfig
        self.Doppler = dopplerConfic
        self.Rotator = rotatorConfig
        self.SDR = sdrConfig
        self.tleUrl = tleUrl

    @classmethod
    def from_file(cls, config_file=os.path.expanduser('~')+'/.config/hsl/config.ini'):
        configParser = ConfigParser()
        configParser.read(config_file)

        satellite = SatelliteConfig(
            configParser.get('Satellite', 'name'),
            configParser.getint('Satellite', 'rxFreq'),
            configParser.getint('Satellite', 'txFreq'),
            configParser.get('Satellite', 'callsign')
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
        rxGain = GainConfig(
            configParser.get('SDR', 'rx_rfGain'),
            configParser.get('SDR', 'rx_ifGain', fallback=None),
            configParser.get('SDR', 'rx_bbGain', fallback=None)
        )
        txGain = None
        if configParser.get('SDR', 'tx_rfGain', fallback=None):
            txGain = GainConfig(
                configParser.get('SDR', 'tx_rfGain'),
                configParser.get('SDR', 'tx_ifGain', fallback=None),
                configParser.get('SDR', 'tx_bbGain', fallback=None)
            )
        sdr = SDRConfig(
            configParser.get('SDR', 'name'),
            configParser.get('SDR', 'samp_rate'),
            rxGain,
            txGain=txGain
        )
        tleUrl = configParser.get('TLE', 'url')
        return cls(
            satellite,
            station,
            doppler,
            rotator,
            sdr,
            tleUrl
        )


class SatelliteConfig(object):
    def __init__(self, name, rxFreq, txFreq, callsign):
        self.name = name
        self.rxFreq = rxFreq
        self.txFreq = txFreq
        self.callsign = callsign

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

class SDRConfig(object):
    def __init__(self, name, samp_rate, rxGain, txGain=None):
        self.name = name
        self.samp_rate = samp_rate
        self.rxGain = rxGain
        self.txGain = txGain

class GainConfig(object):
    def __init__(self, rfGain, ifGain=None, bbGain=None):
        self.rfGain = rfGain
        self.ifGain = ifGain
        self.bbGain = bbGain