import grovepi
import time

def person_detected(max_distance = 50, repeat_times = 5):
    # set I2C to use the hardware bus
    # grovepi.set_bus("RPI_1")

    # Connect the Grove Ultrasonic Ranger to digital port D3
    # SIG,NC,VCC,GND
    ultrasonic_ranger = 3
    
    distance = 0

    for _ in range(repeat_times):
        # try:
            # Read distance value from Ultrasonic
        # distance += grovepi.ultrasonicRead(ultrasonic_ranger)
        print(grovepi.ultrasonicRead(4))

        # except Exception as e:
        #     print ("Ultrasonic Error:{}".format(e))

        time.sleep(0.1) # don't overload the i2c bus
        print(distance)

    if abs(distance / repeat_times) < max_distance:
        print("ultra distance " + str(abs(distance / repeat_times)))
        return True
    else:
        return False


person_detected()