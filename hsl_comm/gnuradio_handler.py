import subprocess
import time
import os

class GnuRadioHandler(object):
    def __init__(self, script_path):
        self.script_path = script_path
        self.args = ['python2', self.script_path]

    def get_args(self):
        process = subprocess.Popen(
            ['python2', self.script_path, '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return(process.communicate())

    def set_args(self, samp_rate=None, rxFreq=None, txFreq=None, callsign=None, rx_rf_gain=None, rx_if_gain=None, rx_bb_gain=None, tx_rf_gain=None, tx_if_gain=None, tx_bb_gain=None, **kwargs):

        # Set arguments if passed (otherwise using defaults in the script)
        if samp_rate:
            self.args += [f'--samp-rate={samp_rate}']
        if rxFreq:
            self.args += [f'--rx-freq={rxFreq}']
        if txFreq:
            self.args += [f'--tx-freq={txFreq}']
        if callsign:
            self.args += [f'--callsign={callsign}']
        if rx_rf_gain:
            self.args += [f'--rx-rf-gain={rx_rf_gain}']
        if rx_if_gain:
            self.args += [f'--rx-if-gain={rx_if_gain}']
        if rx_bb_gain:
            self.args += [f'--rx-bb-gain={rx_bb_gain}']
        if tx_rf_gain:
            self.args += [f'--tx-rf-gain={tx_rf_gain}']
        if tx_if_gain:
            self.args += [f'--tx-if-gain={tx_if_gain}']
        if tx_bb_gain:
            self.args += [f'--tx-bb-gain={tx_bb_gain}']

        # Extra optional arguments
        for key, value in kwargs.items():
            self.args += f'--{key}={value}'

    def start(self):
        self.process = subprocess.Popen(self.args, stdout=subprocess.PIPE, preexec_fn=os.setsid)
    
    def stop(self):
        self.process.kill()
