import time
import grovepi
from collections import Counter

def read_button():

    # Connect the Grove Button to digital port D3
    # SIG,NC,VCC,GND
    button = 4
    grovepi.pinMode(button,"INPUT")
    # avg_press = []
    # for _ in range(5):
    #     try:
    #         press = grovepi.digitalRead(button) 
    #         avg_press.append(press)
    #         time.sleep(0.05)

    #     except IOError:
    #         print ("Error")
    # if Counter(avg_press).most_common(1)[0][0] == 1:
    #     return True
    # else:
    #     return False

    # if grovepi.digitalRead(button):
    #     return True
    # else:
    #     return False
    while True:
        if grovepi.analogRead(button) != 0:
            print('click')
        time.sleep(0.1)

    print(grovepi.analogRead(button))

read_button()