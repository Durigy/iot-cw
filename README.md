# iot-cw

This is our CM2306 comm net project

# Needs:

pip3 inastall mediapipe-rpi4 (for mediapipe to work on the raspberry pi 4)

use the text file: opencv_solutions.txt for setup

use export PATH=$PATH:/home/pi/.local/bin

SETUP:
install all the sudo apt-get dependencies (NOT PIP)
UNinstall numpy
UNinstall pip3 opencv and apt-get opencv
UNinstall opencv-contrib-python

pip3 install opencv-python (WITHOUT SUDO)
pip3 install opencv-contrib-python==4.1.0.25

chmod 777 setup.sh
boi just run setup.sh


# Worked on by:
- Bence Barkanyi
- Somaya Goraine
- Ioannis-Marios Stavropoulos
- Elinor Jones
- Haoyu Yin
- Alex Deverson
