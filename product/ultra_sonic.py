import grovepi
import time

def person_detected(max_distance = 50, repeat_times = 5):
    # set I2C to use the hardware bus
    # grovepi.set_bus("RPI_1")

    # Connect the Grove Ultrasonic Ranger to digital port D3
    # SIG,NC,VCC,GND
    ultrasonic_ranger = 3
    
    distance = 0

    # collect data and find average later on
    for _ in range(repeat_times):
        try:
            # Read distance value from Ultrasonic
            distance += grovepi.ultrasonicRead(ultrasonic_ranger)
            # print(grovepi.ultrasonicRead(ultrasonic_ranger))

        except Exception as e:
            print ("Ultrasonic Error:{}".format(e))

        time.sleep(0.05) # don't overload the i2c bus
        # print(distance)

    # if distance detected is less than the pre-set 50cm, it means that the door is opened (so a person will be entering)
    if abs(distance / repeat_times) < max_distance:
        # print("ultra distance " + str(abs(distance / repeat_times)))
        return True
    else:
        return False

if __name__ == '__main__':
    print(person_detected())