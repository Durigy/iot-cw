from lcd import setText
from buzzer import buzzer
# from button import read_button
import mediapipe as mp
import time
from ultra_sonic import person_detected
import threading as t
from vision import get_finger_count
# from light import sort_light
from light import sort_light, turn_light_off
import requests
import json
from verify_password import check_password, setup_password
from datetime import datetime


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands = 1, min_detection_confidence=0.70)

unlocked = False
countdown_over = False
stop_countdown_for_disarmed = False

api_key = '851db27bf1b1c6a0dc8f' #ae2ce6622d27d55654d784614e77'
url = 'https://5qu.me/api/'
device_name = "Security System 1"
device_id = ''
unlocked = False


def start_countdown_for_alarm(countdown, light_turned_on):
    global unlocked
    start = time.time()
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

    global unlocked

    unlocked = False

    while True:
        if person_detected():
            # check the lights and turn them on
            light_turned_on = sort_light()

            # global unlocked, countdown_over
            countdown = 60
            # unlocked = False
            thread = t.Thread(target=start_countdown_for_alarm, args=[countdown, light_turned_on])
            thread.start()

            while True:
                if check_password(mp_hands, mp_draw, hands, url, api_key, device_id):
                    break
            # thread.join()
            break
        time.sleep(0.02)

    # at this point the password will have been accepted
    
    if light_turned_on:
        turn_light_off()

    r = requests.post(url+'device/send_data', data = {
        'device_id': device_id,
        'api_key':api_key,
        'light': light_turned_on,
        'time': datetime.utcnow,
        'is_intruder': False
    })

    disarmed_mode()

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
    global unlocked, countdown_over, stop_countdown_for_disarmed
    unlocked = True
    setText('[DISARMED]', 'green')
    time.sleep(2.5)
    setText('', 'off')
    countdown = 5
    while True:
        if person_detected():
            countdown_over = False
            setText("5: Armed Mode")
            thread = t.Thread(target=start_countdown_for_disarmed, args=[countdown])
            thread.start()
            while not countdown_over:
                if get_finger_count(mp_hands, mp_draw, hands) == 5:
                    stop_countdown_for_disarmed = True
                    break
            # thread.join()
            if countdown_over:
                setText('', 'off')
                continue
            else:
                break

        time.sleep(0.02)
        

    armed_mode()

def set_off_alarm(light_turned_on):
    # set off alarm and continuously check global unlock variable to turn it off

    r = requests.post(url+'device/send_data', data = {
        'device_id': device_id,
        'api_key':api_key,
        'light': light_turned_on,
        'time': datetime.utcnow,
        'is_intruder': True
    })

    global unlocked
    while True:
        print(unlocked)
        if not unlocked:
            buzzer('-----')
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
    if result[0]:
        device_id = result[1]

    # disarmed_mode()

    armed_mode()




    # if person_detected():
    #     print('hello world')
    #     sort_light()
    #     setText('Enter your\nPassword')
    #     working_pwd = get_password(mp_hands, mp_draw, hands, pass_count=4)
    #     setText(f'[ACCESS GRANTED]\n{str(working_pwd)}', 'green')



main()