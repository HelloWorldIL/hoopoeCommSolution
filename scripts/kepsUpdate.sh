#!/usr/bin/env bash

wget -qr www.celestrak.com/NORAD/elements/cubesat.txt -O $HOME/.hoopoe/cubesat.txt
cat $HOME/.hoopoe/cubesat.txt | grep -P 'HOOPOE' -A 2 > $HOME/.hoopoe/HOOPOE.txt
