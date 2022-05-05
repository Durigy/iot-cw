import time
import os
import threading as t

def ex():
    time.sleep(10)
    os.system('python3 /home/pi/iotproduct/iot-cw/product/main.py')

thread = t.Thread(target = ex)
thread.start()
