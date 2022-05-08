from lcd import setText
from buzzer import buzzer
# from button import read_button
import mediapipe as mp
import time
from ultra_sonic import person_detected
import threading as t
from vision import get_finger_count, get_finger_count_with_time_restriction
# from light import sort_light
from light import sort_light, turn_light_off
import requests
import json
from verify_password import check_password, setup_password
from datetime import datetime


# arguments to pass to vision.py to detect hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands = 1, min_detection_confidence=0.70)


unlocked = False # device is locked/unlocked
countdown_over = False # when disarmed and a person is detected, after some time this becomes true and is used as a flag to turn the display off
stop_countdown_for_disarmed = False # used in the same context as countdown_over, but it becomes true if the user arms the device, instead of ignoring it

# each device has a unique api key, but because this is a prototype and this is currently the only device that exists,
# this api key is pre-determined and is assigned statically here
api_key = '851db27bf1b1c6a0dc8f' #ae2ce6622d27d55654d784614e77'
url = 'https://5qu.me/api/' # home server that sends and receives data to and from the pi
device_name = "Security System 1" # again static name because this is a prototype
device_id = '' # if this is a new device the device id is generated from the server and is stored in device_id.txt
# otherwise, if the device is already assigned an id, it is recovered from the file
unlocked = False


# function that is run by a thread while the user is entering their password
# if after a minute (or a given countdown) the user has not entered the correct password, it sets of the alarm
def start_countdown_for_alarm(countdown, light_turned_on):
    global unlocked
    start = time.time()

    # constantly check if the device has been unlocked by reading the 'unlocked' flag
    while time.time() - start < countdown and not unlocked:
        continue
    if unlocked:
        exit()
        # return
    else:
        # prioritize setting off the alarm then return to the caller
        set_off_alarm(light_turned_on)
        exit()


def armed_mode():
    buzzer('--')
    setText('[ARMED]', 'red')
    time.sleep(1.5)
    setText('', 'off')

    try:
        # log that the device is armed by sending info to the server
        r2 = requests.put(url+'device', data = {
            'device_id': device_id,
            'api_key': api_key,
            'is_armed': '1'
        })
        # print(r2.json())
    except:
        pass
    
    # print(device_id)
    # print(api_key)
    global unlocked

    unlocked = False
    light_turned_on = ''


    while True:
        # constantly check for movement
        if person_detected():
            # check the lights and turn them on
            light_turned_on = '' if not sort_light() else 1
            print('from  main ' + str(light_turned_on))

            # global unlocked, countdown_over
            countdown = 60
            # unlocked = False

            # start a new thread that keeps track of time and sets off the alarm if if the user has not enter the correct password after some time
            thread = t.Thread(target=start_countdown_for_alarm, args=[countdown, light_turned_on])
            thread.start()

            while True:
                # if the correct password is inputted
                if check_password(mp_hands, mp_draw, hands, url, api_key, device_id):
                    break
            # thread.join()
            break
        time.sleep(0.02)

    # at this point the password will have been accepted
    
    if light_turned_on:
        turn_light_off()


    try:
        # log to the server - send is_intruder as false
        r = requests.post(url+'device/send_data', data = {
            'device_id': device_id,
            'api_key':api_key,
            'light': light_turned_on,
            'time': datetime.utcnow(),
            'is_intruder': ''
        })
    except:
        pass

    try:
        #notify server that device is disarmed
        r3 = requests.put(url+'device', data = {
            'device_id': device_id,
            'api_key':api_key,
            'is_armed': ''
        })

        # print(r3.json())
    except:
        pass

    disarmed_mode()

# sets countdown_over and stop_countdown_for_disarmed flags true or false, which are used
# to either arm the device or turn off the display if the user does not arm it
def start_countdown_for_disarmed(countdown):
    global countdown_over, stop_countdown_for_disarmed
    start = time.time()
    while time.time() - start < countdown and not stop_countdown_for_disarmed:
        continue
    
    if stop_countdown_for_disarmed:
        stop_countdown_for_disarmed = False
        exit()

    countdown_over = True
    exit()

def disarmed_mode():
    global unlocked, stop_countdown_for_disarmed
    unlocked = True
    setText('[DISARMED]', 'green')
    time.sleep(2.5)
    setText('', 'off')
    countdown = 5
    while True:
        # constantly detect movement 
        if person_detected():
            global countdown_over
            countdown_over = False
            # call sort_light to turn lights on if needed so the camera can detect the user's gestures
            sort_light()
            setText("5: Armed Mode")
            thread = t.Thread(target=start_countdown_for_disarmed, args=[countdown]) # thread that keeps track of time and sets flag to turn the display off to true if needed
            thread.start()
            while not countdown_over:
                # call the function below instead of normal get_finger_count otherwise the device will be stuck if it does not detect a gesture (in case user did not actually want to arm the device and they just ignored it)
                if get_finger_count_with_time_restriction(mp_hands, mp_draw, hands) == 5:
                    stop_countdown_for_disarmed = True
                    break
            # thread.join()

            turn_light_off()

            # if true, user did not want to arm the device, so turn off display and continue with the loop
            if countdown_over:
                setText('', 'off')
                continue
            else:
                break

        time.sleep(0.02)

    armed_mode()

def set_off_alarm(light_turned_on):
    # set off alarm and continuously check global unlock variable to turn it off

    try:
        # when the alarm is set off, notify server that there is an intruder
        r = requests.post(url+'device/send_data', data = {
            'device_id': device_id,
            'api_key':api_key,
            'light': light_turned_on,
            'time': datetime.utcnow(),
            'is_intruder': '1'
        })
    except:
        pass

    global unlocked
    while True:
        print(unlocked)
        # constantly check if password is inputted correctly by the user
        if not unlocked:
            buzzer('-----') #sound the alarm
        else:
            break
        time.sleep(1)
    # disarmed_mode()


# for testing use password as a global variable
password = ''
def main():

    setText('', 'white')

    # api_key = '851db27bf1b1c6a0dc8f' #ae2ce6622d27d55654d784614e77'
    # url = 'https://5qu.me/api/'
    # device_name = "Security System 1"
    # device_id = ''
    # unlocked = False

    # r = requests.post(f'{url}device', data = {
    #     'hashed_password': 'hashed_password_string',
    #     'api_key':api_key,
    #     'name': device_name,
    #     'is_armed': not unlocked
    #     })
    
    # global device_id
    # device_id = r.json()['id']

    # print(r.json())
    global device_id
    result = setup_password(mp_hands, mp_draw, hands, url, api_key, device_name, unlocked)
    # result is (Boolean, String) tuple

    if result[0]:
        # this means the device is being turned on for the first time and a device id is generated from it by the server
        device_id = result[1]
    else:
        try:
            # this means the device has already been registered and has a device_id, so we need to read it from device_id.txt
            f = open("device_id.txt", 'r')
            device_id = f.read()
            f.close()
        except:
            pass

    # disarmed_mode()

    # go straight into armed mode (password for device has just been created or it has already been set up, so either way, go into armed mode)
    armed_mode()




    # if person_detected():
    #     print('hello world')
    #     sort_light()
    #     setText('Enter your\nPassword')
    #     working_pwd = get_password(mp_hands, mp_draw, hands, pass_count=4)
    #     setText(f'[ACCESS GRANTED]\n{str(working_pwd)}', 'green')



main()