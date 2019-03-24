#!/bin/sh
DEPENDENCIES="python-pip python3-pip git cmake build-essential g++ python-mako python-six libogg-dev libvorbis-dev libpng-dev libpng++-dev"

sudo apt update
sudo apt install -y $DEPENDENCIES
pip install git+https://github.com/gnuradio/pybombs.git

pip3 install numpy
pip3 install scipy
pip3 install skyfield

pip install scipy

sudo apt install -y gpredict

# pybombs setup in gnuradio installation
pybombs auto-config
pybombs recipes add-defaults
pybombs prefix init ~/prefix -a main -R gnuradio-default
pybombs install gr-satellites
pybombs install gr-bruninga
pybombs install gr-limesdr
pybombs install gr-osmosdr
pybombs install gqrx

# Copy default config file to default config directory at ~/.hslCommSolution
mkdir ~/.hslCommSolution
cp config.ini ~/.hslCommSolution

# gr-satnogs install
cd ~/prefix/src
git clone https://gitlab.com/librespacefoundation/satnogs/gr-satnogs.git
cd gr-satnogs
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=~/prefix ..
make
sudo make install
cd

cd ~/prefix/src/gr-satellites
./compile_hierarchical.sh
cd