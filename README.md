# hoopoeCommSolution
A collection of scripts and resources to decode the HOOPOE satellites

(Linux filesystem) Place Config file at: ~/.hslCommSolution/config.ini

## Installation
In the future, there will be a docker file and proper installation scrips to automate the installation, for now, follow the instructions below:

### Dependencies
- Gnu Radio (PyBombs)
- gr-osmosdr (PyBombs)
- gr-limesdr (PyBombs)
- gr-satellites (PyBombs)
- gr-bruninga (PyBombs)
- [gr-satnogs](https://gitlab.com/librespacefoundation/satnogs/gr-satnogs) (Build using cmake)
- scipy (Python2)
- SkyField (Python3)

The GnuRadio flowgraphs were tested on GnuRadio installed using [PyBombs](https://github.com/gnuradio/pybombs)**
To install GnuRadio using PyBombs, you first need to install PyBombs using pip.
**The installation instructions are made for (Debian / Ubuntu)**

**Installation from source takes a long time!**

Install pip:
```bash
$ [sudo] apt install python-pip
$ [sudo] apt install python3-pip
```
Then install PyBombs:
```bash
$ pip install git+https://github.com/gnuradio/pybombs.git
```
Now initialize a PyBombs prefix and install GnuRadio and GnuRadio packages
```bash
$ pybombs auto-config
$ pybombs recipes add-defaults # Adds default recipes
$ pybombs prefix init ~/prefix -a default -R gnuradio-default # Initializes default prefix and installs GnuRadio
$ pybombs install gr-satellites
$ pybombs install gr-bruninga
$ pybombs install gr-limesdr
$ pybombs install gr-osmosdr
```
Next install gr-satnogs using build instructions on the [GitLab page for gr-satnogs](https://github.com/gnuradio/pybombs):
```bash
cd ~/prefix/src
git clone https://gitlab.com/librespacefoundation/satnogs/gr-satnogs.git
cd gr-satnogs
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=~/prefix ..
make
sudo make install
cd
```

The flowgraphs depend on an AGC in the hierarchical flowgraphs in gr-satellites, to compile the flowgraphs in gr-satellites:
```bash
source ~/prefix/setup_env.sh # Activate prefix
cd ~/prefix/src/gr-satellites
./compile_hierarchical.sh
cd
```

Install other dependencies (apt and pip):
```bash
# Python2
pip3 install scipy
pip3 install skyfield
pip3 install requests

# Python3
pip install scipy
pip install requests
```

Lastly, copy the default config.ini file to the default location (~/.hslCommSolution/config.ini)
```bash
mkdir ~/.hslCommSolution
cp config.ini ~/.hslCommSolution
```

## Flowgraphs
- **flowgraphs/production/afsk_ax25_tx.grc** - hierarchical block that outputs an AX.25 AFSK packet *Will be remade in the future more cleanly.
- **flowgraphs/production/bpsk_ax25.grc** - hierarchical block that receives AX.25 BPSK packets (Outputs packets in KISS format).
- **flowgraphs/production/limesdr_gui.grc** - Complete array (tx: AX.25 AFSK rx: AX.25 BPSK) using LimeSDR.
- **/flowgraphs/ax25BPSK_TX.grc** - AX.25 BPSK transmitter (using LimeSDR).

## Scripts
- **scripts/predict.py** - Python doppler prediction script (reads from config.ini at the default config location)
- **scripts/install.sh** - Bash installation script (Currently not up-to-date and not tested)

## TODO:
Tasks for the project

### Gnu Radio & DSP
- [x] Build an AX.25 BPSK decoder
- [x] Build an AX.25 AFSK transmitter at FM Mode
- [x] Add Doppler correction blocks

### Production
- [x] Create a unified communication flowgraph
- [ ] Create production and testing flowgraphs
- [x] Create flowgraph for LimeSDR
- [x] Create RX only flowgraph with osmocom I.E: RTL-SDR
- [x] Create flowgraph with osmocom for device support

### Scripts
- [x] Create Doppler Correction script
- [ ] Create installation script

### General
- [ ] Add documentation
- [ ] Add DOCKERFILE