import grovepi
import time

# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
ultrasonic_ranger = 3

def person_detected(repeat_times = 5):
    distance = 0
    for _ in range(repeat_times):
        try:
            # Read distance value from Ultrasonic
            distance += grovepi.ultrasonicRead(ultrasonic_ranger)

        except Exception as e:
            print ("Error:{}".format(e))

        time.sleep(0.1) # don't overload the i2c bus
    return abs(distance / repeat_times)
