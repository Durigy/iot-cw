import grovepi
import time

# actuator - used to provide audio feedback to the user
# takes in a string of any length that consists of '.' (short sound) '-' long sound
# and plays back the audio
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
