import time
import grovepi
# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
light_sensor = 0
# Connect the LED to digital port D4
# SIG,NC,VCC,GND
led = 4
 

def sort_light(threshold = 500, repeat_times = 3):
    grovepi.pinMode(light_sensor,"INPUT")
    grovepi.pinMode(led,"OUTPUT")

    sensor_value = 0
    
    for _ in range(repeat_times):
        try:
            # Get sensor value
            sensor_value += grovepi.analogRead(light_sensor)
            # Calculate resistance of sensor in K
            # resistance = (float)(1023 - sensor_value) * 10 / sensor_value
            time.sleep(0.05)
        except IOError:
            print ("Error")
            return (-1)

    v = abs(sensor_value / repeat_times)
    print(v)

    if v < threshold:
        # Send HIGH to switch on LED
        # grovepi.digitalWrite(led,1)
        turn_light_on()
        return True
    else:
        # Send LOW to switch off LED
        # grovepi.digitalWrite(led,0)
        turn_light_off()
        return False

def turn_light_off():
    grovepi.digitalWrite(led,0)

def turn_light_on():
    grovepi.digitalWrite(led,1)
