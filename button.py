import re
import time
import grovepi
from collections import Counter

# Connect the Grove Button to digital port D3
# SIG,NC,VCC,GND
button = 2
grovepi.pinMode(button,"INPUT")

def read_button():
    avg_press = []
    for _ in range(5):
        try:
            press = grovepi.digitalRead(button) 
            print(press)
            avg_press.append(press)
            time.sleep(0.05)

        except IOError:
            print ("Error")
    if Counter(avg_press).most_common(1)[0][0] == 1:
        return True
    else:
        return False
    