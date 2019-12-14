from setuptools import setup

setup(name='hsl_comm',
      version='0.1',
      description='The Hoopoe communication solution python package',
      url='https://github.com/HelloWorldIL/hoopoeCommSolution',
      author='Ido Bronfeld',
      author_email='idobronfeld@gmail.com',
      license='MIT',
      packages=['hsl_comm'],
      scripts=['scripts/hsl_doppler_rotator_control'],
      zip_safe=False)