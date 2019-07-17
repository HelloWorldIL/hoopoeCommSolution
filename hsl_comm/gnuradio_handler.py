import subprocess
import time
import os

class GnuRadioHandler(object):
    def __init__(self, script_path):
        self.script_path = script_path
        self.args = ['python2', self.script_path]

    def get_args(self):
        process = subprocess.Popen(
            ['python2', self.script_path, '--help'])
        return(process.communicate())

    def set_args(self,**kwargs):
        for key, value in kwargs.items():
            self.args += f'--{key}={value}'

    def start(self):
        self.process = subprocess.Popen(self.args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, preexec_fn=os.setsid)
        time.sleep(2)
        if self.process.poll() is not None:
            self.process.kill()
            raise Exception('The process crashed! Check if you device is connected.')

    def stop(self):
        self.process.stdin.write(b'\n')
        self.process.stdin.flush()
        self.process.kill()
