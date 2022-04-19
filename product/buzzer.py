import grovepi
import time

def buzzer(code, dur = 0.01):
    buzzer = 8

    grovepi.pinMode(buzzer, 'OUTPUT')

    for i in code:
        if i == '.':
            grovepi.digitalWrite(buzzer, 1)
            time.sleep(0.01)
            grovepi.digitalWrite(buzzer, 0)
            time.sleep(0.5)
        elif i == '-':
            grovepi.digitalWrite(buzzer, 1)
            time.sleep(0.06)
            grovepi.digitalWrite(buzzer, 0)
            time.sleep(0.5)
