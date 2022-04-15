"""
/***************************************************************************
* Sketch Name: Lab1_code1
* Description: Arduino - Grove_Pi_Sensors
* Parameters: PIR, Light, Button, LED
* Return: Dark, Light, Movement, Watching
* Copyright: Following code is written for educational purposes by Cardiff University.
* Latest Version: 05/08/2021 (by Hakan KAYAN)
* Modified from: https://github.com/DexterInd/GrovePi.git

* Adapted by group 13
***************************************************************************/
"""

import time
import sys
# import os
# import grovepi
# import math
# import json

# CONNECT LCD TO I2C-2

sensor = 4  # The Sensor goes on digital port 4.
blue = 0    # The Blue colored sensor.

if sys.platform == 'uwp':
    import winrt_smbus as smbus
    bus = smbus.SMBus(1)
else:
    import smbus
    import RPi.GPIO as GPIO
    rev = GPIO.RPI_REVISION
    if rev == 2 or rev == 3:
        bus = smbus.SMBus(1)
    else:
        bus = smbus.SMBus(0)

# this device has two I2C addresses
DISPLAY_TEXT_ADDR = 0x3e

DISPLAY_RGB_ADDR = 0x62

# set backlight to (R,G,B) (values from 0..255 for each)
def setRGB(r,g,b):
    bus.write_byte_data(DISPLAY_RGB_ADDR,0,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,1,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR,4,r)
    bus.write_byte_data(DISPLAY_RGB_ADDR,3,g)
    bus.write_byte_data(DISPLAY_RGB_ADDR,2,b)

# send command to display (no need for external use)    
def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)


# set display text \n for second line(or auto wrap)     
def setText(text, color='white'):

    if color == 'red':
        setRGB(255, 0 , 0)
    elif color == 'green':
        setRGB(0, 255, 0)
    elif color == 'blue':
        setRGB(100, 100 , 255)
    elif color == 'white':
        setRGB(255, 255, 255)
    elif color == 'purple':
        setRGB(155, 30, 155)
    elif color == 'off':
        setRGB(0, 0, 0)

    textCommand(0x01) # clear display
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))
